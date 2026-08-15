#!/usr/bin/env python3
"""
Fetch the text of a URL so it can be summarised.

Handles the awkward cases so the model doesn't have to reinvent them:
video transcripts, PDFs, and ordinary web pages. Everything is optional --
if a tool isn't installed, this degrades to the next best method and tells
you plainly what it could and couldn't do.

Usage:
    python3 get_content.py <url-or-path> [--max-chars N]

Exit codes:
    0  got usable text (printed to stdout)
    2  reached the URL but could not extract text (paywall, JS-only, no captions)
    3  could not reach the source at all

Output is always: a short "===== SOURCE =====" header block with metadata,
then the extracted text. Read the header -- it tells you how the text was
obtained, which matters when judging how much to trust it.
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"

VIDEO_HOSTS = (
    "youtube.com", "youtu.be", "vimeo.com", "loom.com",
    "tiktok.com", "instagram.com", "twitter.com", "x.com",
)

# ffmpeg is frequently installed somewhere that isn't on PATH for GUI-launched
# processes. Probe the usual suspects before giving up on local transcription.
FFMPEG_HINTS = [
    os.path.expanduser("~/Library/Python/3.9/bin"),
    "/opt/homebrew/bin",
    "/usr/local/bin",
    "/usr/bin",
]


def ensure_ffmpeg_on_path():
    if shutil.which("ffmpeg"):
        return True
    for d in FFMPEG_HINTS:
        if os.path.exists(os.path.join(d, "ffmpeg")):
            os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")
            return True
    return False


def emit(text, method, source, note=""):
    print("===== SOURCE =====")
    print(f"source: {source}")
    print(f"method: {method}")
    if note:
        print(f"note: {note}")
    print(f"chars: {len(text)}")
    print("===== CONTENT =====")
    print(text)


def fail(code, source, reason, suggestion=""):
    print("===== SOURCE =====")
    print(f"source: {source}")
    print("method: FAILED")
    print(f"reason: {reason}")
    if suggestion:
        print(f"suggestion: {suggestion}")
    sys.exit(code)


def is_video(url):
    return any(h in url.lower() for h in VIDEO_HOSTS)


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get_content_type()


# --------------------------------------------------------------------------
# Video
# --------------------------------------------------------------------------

def video_text(url):
    """Captions first (cheap, exact), then local transcription (slow, works offline)."""
    if not shutil.which("yt-dlp"):
        return None, None, "yt-dlp not installed"

    tmp = tempfile.mkdtemp(prefix="summarize-")
    try:
        # Stage 1: subtitles. Manual subs beat auto-generated, both beat nothing.
        subprocess.run(
            ["yt-dlp", "--skip-download", "--write-sub", "--write-auto-sub",
             "--sub-lang", "en.*", "--sub-format", "vtt/srt/best",
             "-o", os.path.join(tmp, "cap"), url],
            capture_output=True, timeout=180,
        )
        caps = [f for f in os.listdir(tmp) if f.endswith((".vtt", ".srt"))]
        if caps:
            # Prefer a manual track if one came down alongside the auto track.
            caps.sort(key=lambda f: ("auto" in f, f))
            with open(os.path.join(tmp, caps[0]), encoding="utf-8", errors="replace") as fh:
                text = strip_captions(fh.read())
            if text.strip():
                kind = "auto-generated" if "auto" in caps[0] else "human-written"
                return text, f"video captions ({kind})", None

        # Stage 2: pull the audio and transcribe it locally.
        try:
            import mlx_whisper  # noqa: F401
        except ImportError:
            return None, None, "no captions available and mlx-whisper not installed"
        if not ensure_ffmpeg_on_path():
            return None, None, "no captions available and ffmpeg not found"

        audio = os.path.join(tmp, "audio.m4a")
        r = subprocess.run(
            ["yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "m4a",
             "-o", audio, url],
            capture_output=True, timeout=600,
        )
        if r.returncode != 0 or not os.path.exists(audio):
            return None, None, "no captions available and audio download failed"

        import mlx_whisper
        res = mlx_whisper.transcribe(
            audio, path_or_hf_repo="mlx-community/whisper-large-v3-mlx", verbose=False
        )
        return res["text"].strip(), "local transcription (whisper-large-v3)", None
    except subprocess.TimeoutExpired:
        return None, None, "video processing timed out"
    except Exception as e:  # noqa: BLE001 - report, don't crash
        return None, None, f"video processing failed: {e}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def strip_captions(raw):
    """VTT/SRT -> plain prose, with the duplicate lines auto-captions love removed."""
    out, seen_last = [], None
    for line in raw.splitlines():
        line = line.strip()
        if (not line or line == "WEBVTT" or line.isdigit()
                or "-->" in line or line.startswith(("Kind:", "Language:", "NOTE"))):
            continue
        line = re.sub(r"<[^>]+>", "", line)          # inline timing tags
        line = re.sub(r"\[[^\]]*\]", "", line).strip()  # [Music], [Applause]
        if line and line != seen_last:
            out.append(line)
            seen_last = line
    return " ".join(out)


# --------------------------------------------------------------------------
# PDF + HTML
# --------------------------------------------------------------------------

def pdf_text(data):
    try:
        import pypdf
    except ImportError:
        return None
    try:
        import io
        reader = pypdf.PdfReader(io.BytesIO(data))
        return "\n\n".join((p.extract_text() or "") for p in reader.pages).strip()
    except Exception:  # noqa: BLE001
        return None


def html_text(markup):
    """Strip chrome and tags. Crude, but predictable and dependency-free."""
    markup = re.sub(r"(?is)<(script|style|nav|footer|header|aside|form|noscript)\b.*?</\1>", " ", markup)
    markup = re.sub(r"(?is)<!--.*?-->", " ", markup)
    markup = re.sub(r"(?i)<(br|/p|/div|/li|/h[1-6]|/tr)\s*/?>", "\n", markup)
    text = re.sub(r"(?s)<[^>]+>", " ", markup)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--max-chars", type=int, default=200_000)
    args = ap.parse_args()
    t = args.target

    # Local file
    if not t.startswith(("http://", "https://")):
        if not os.path.exists(t):
            fail(3, t, "file not found")
        if t.lower().endswith(".pdf"):
            with open(t, "rb") as fh:
                text = pdf_text(fh.read())
            if not text:
                fail(2, t, "could not extract PDF text",
                     "install pypdf, or read the file directly with the Read tool")
            emit(text[:args.max_chars], "local PDF", t)
            return
        with open(t, encoding="utf-8", errors="replace") as fh:
            emit(fh.read()[:args.max_chars], "local file", t)
        return

    # Video
    if is_video(t):
        text, method, why = video_text(t)
        if text:
            emit(text[:args.max_chars], method, t)
            return
        fail(2, t, why or "could not get video text",
             "try fetching the page normally for a description, or ask the user to paste a transcript")

    # Web page / remote PDF
    try:
        data, ctype = http_get(t)
    except urllib.error.HTTPError as e:
        hint = ("looks like a paywall or bot block -- try the WebFetch tool, "
                "or ask the user to paste the text") if e.code in (401, 402, 403, 429) else ""
        fail(3, t, f"HTTP {e.code}", hint)
    except Exception as e:  # noqa: BLE001
        fail(3, t, f"could not reach source: {e}")

    if "pdf" in (ctype or "") or t.lower().endswith(".pdf"):
        text = pdf_text(data)
        if not text:
            fail(2, t, "remote PDF but no PDF parser available", "install pypdf")
        emit(text[:args.max_chars], "remote PDF", t)
        return

    markup = data.decode("utf-8", errors="replace")
    text = html_text(markup)
    # A short page is fine. A *big* page that yields almost no text is the real
    # tell for a paywall or a JS-only render, so compare the two.
    if not text or (len(markup) > 20_000 and len(text) < 600):
        fail(2, t, f"only {len(text)} chars of text from {len(markup)} chars of HTML "
                   f"-- likely JS-rendered or paywalled",
             "try the WebFetch tool or a browser, which handle JS and cookies")
    emit(text[:args.max_chars], "web page", t)


if __name__ == "__main__":
    main()
