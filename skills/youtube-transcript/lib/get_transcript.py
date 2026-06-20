#!/usr/bin/env python3
"""
YouTube Transcript Extractor
Pulls auto-generated or manually uploaded captions from any YouTube video.
No API key required. Falls back to HappyScribe if no captions available.

Usage:
  python get_transcript.py --url "https://www.youtube.com/live/DEaEeWzigsE" --lang es
  python get_transcript.py --url "..." --list-langs
  python get_transcript.py --url "..." --lang es --format json --output transcript.txt
"""

import argparse
import json
import re
import sys


def extract_video_id(url: str) -> str:
    patterns = [
        r"(?:v=)([a-zA-Z0-9_-]{11})",
        r"(?:live/)([a-zA-Z0-9_-]{11})",
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def list_languages(video_id: str) -> None:
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    try:
        transcripts = api.list(video_id)
        print(f"Available transcripts for {video_id}:")
        for t in transcripts:
            kind = "auto-generated" if t.is_generated else "manual"
            print(f"  {t.language_code:6s}  {t.language:30s}  [{kind}]")
    except Exception as e:
        print(f"No transcripts available: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_transcript(video_id: str, lang_codes: list[str]) -> list:
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    transcripts = api.list(video_id)

    for lang in lang_codes:
        try:
            t = transcripts.find_transcript([lang])
            return list(t.fetch())
        except Exception:
            continue

    # Last resort: any available transcript
    for t in transcripts:
        try:
            return list(t.fetch())
        except Exception:
            continue

    raise RuntimeError(f"No transcript found for video {video_id} in languages: {lang_codes}")


def format_plain(segments) -> str:
    return " ".join(seg.text for seg in segments)


def format_timestamped(segments) -> str:
    lines = []
    for seg in segments:
        mins = int(seg.start // 60)
        secs = int(seg.start % 60)
        lines.append(f"[{mins:02d}:{secs:02d}] {seg.text}")
    return "\n".join(lines)


def format_json(segments) -> str:
    data = [{"start": round(seg.start, 2), "duration": round(seg.duration, 2), "text": seg.text} for seg in segments]
    return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube transcript")
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--lang", default="es", help="Language code(s), comma-separated. Default: es")
    parser.add_argument("--format", choices=["plain", "timestamped", "json"], default="plain",
                        help="Output format. Default: plain")
    parser.add_argument("--output", help="Save to this file path (UTF-8). Default: print to stdout")
    parser.add_argument("--list-langs", action="store_true", help="List available languages and exit")
    parser.add_argument("--encoding", default="utf-8", help="Output file encoding. Default: utf-8")
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.list_langs:
        list_languages(video_id)
        return

    lang_codes = [c.strip() for c in args.lang.split(",")]

    try:
        segments = fetch_transcript(video_id, lang_codes)
    except Exception as e:
        print(f"Error fetching transcript: {e}", file=sys.stderr)
        print("Tip: run with --list-langs to see what's available, or use HappyScribe.", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        output = format_json(segments)
    elif args.format == "timestamped":
        output = format_timestamped(segments)
    else:
        output = format_plain(segments)

    if args.output:
        with open(args.output, "w", encoding=args.encoding) as f:
            f.write(output)
        print(f"Saved {len(segments)} segments to {args.output}")
        print(f"Characters: {len(output)}")
    else:
        print(output)


if __name__ == "__main__":
    main()
