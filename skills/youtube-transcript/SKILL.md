---
name: youtube-transcript
description: Extract the transcript from any YouTube video (live or recorded) using auto-generated captions. Free, instant, no HappyScribe credits. Use for podcast episodes, interviews, or any YouTube URL before feeding into the content pipeline.
metadata:
  short-description: Pull YouTube captions as clean text — free, no upload, no credits
---

# YouTube Transcript — WAT Skill

## Trigger

Natural language: "get the transcript for this YouTube video", "extract transcript from YouTube URL",
"pull captions from this YouTube link", "transcribe this YouTube episode",
"get the text from this YouTube live"

Slash command: `/youtube-transcript`

## Goal

Extract a clean timestamped transcript from any YouTube video using its auto-generated or manually uploaded captions — no HappyScribe upload, no API credits, no human copy-paste from a website.

Preferred output: plain text block (for feeding into Claude content pipeline)
Optional output: JSON with timestamps (for fine-grained editing or subtitle sync)

## Environment

**Dependency:** `youtube-transcript-api` Python library (already installed on Leo's machine)

```powershell
# Verify installed:
python -m pip show youtube-transcript-api

# Install if missing:
pip install youtube-transcript-api
```

**No API key required.** Works for any public YouTube video that has captions (auto-generated or manually uploaded).

## Step-by-Step Process

1. **Receive the YouTube URL** — any format accepted:
   - `https://www.youtube.com/watch?v=VIDEO_ID`
   - `https://www.youtube.com/live/VIDEO_ID`
   - `https://youtu.be/VIDEO_ID`

2. **Run the extraction script:**

   ```powershell
   # Plain text output (default — best for content pipeline)
   python "C:\Users\Leo\ai-skills\skills\youtube-transcript\lib\get_transcript.py" \
     --url "https://www.youtube.com/live/DEaEeWzigsE" \
     --lang es

   # Save to file
   python "C:\Users\Leo\ai-skills\skills\youtube-transcript\lib\get_transcript.py" \
     --url "https://www.youtube.com/live/DEaEeWzigsE" \
     --lang es \
     --output "C:\Users\Leo\clients\leo-content\video-content\Pending\2026-06-20_podcast_ep4.txt"

   # JSON with timestamps
   python "C:\Users\Leo\ai-skills\skills\youtube-transcript\lib\get_transcript.py" \
     --url "..." --lang es --format json
   ```

3. **Check available languages** (if transcript fetch fails):

   ```powershell
   python "C:\Users\Leo\ai-skills\skills\youtube-transcript\lib\get_transcript.py" \
     --url "..." --list-langs
   ```

4. **Feed into the content pipeline:**
   - Save the `.txt` output to `video-content\Pending\`
   - Run `python video_pipeline.py --source "STEM"` as normal
   - Pipeline uses the text as the source transcript (skips HappyScribe)

## Language Defaults

| Channel | Default lang |
|---------|-------------|
| Negocios Sin Miedo (Leo's podcast) | `es` |
| DigitalTrack educational / English content | `en` |
| Bilingual — try Spanish first, fall back to English | `es,en` (comma-separated, script tries in order) |

## Rules

- **Use this before HappyScribe** — if the video has auto-captions, this is free and instant
- **HappyScribe fallback:** if `--list-langs` returns nothing or the fetch fails, upload the audio to HappyScribe via the `/video` skill instead
- **Privacy:** do not save raw transcripts with client names, cities, or identifying details to public paths — follow topic hint privacy rules in `leo-content/CLAUDE.md`
- **Quality note:** auto-generated captions drop filler words inconsistently. For final published clips, validate key quotes against the audio
- **Live video:** works for YouTube Live replays as long as YouTube has generated captions (usually available within a few minutes of stream end)

## Self-Improvement Loop

- If a video has no available transcripts, log it and fall back to HappyScribe automatically
- If special characters appear garbled (ñ, á, é), ensure the output file is saved as UTF-8: `--encoding utf-8` flag (default)
- Test with the Negocios Sin Miedo episode after each podcast recording to confirm captions are live before kicking off the pipeline
