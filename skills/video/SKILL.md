# Leo Content Pipeline — Video Skill

This skill covers the full video production workflow for Leo's social content:
Pexels stock video + ElevenLabs cloned voice (JSON2Video bootstrap) → Remotion final pass (centered DT text).

**Project root:** `C:\Users\Leo\clients\leo-content`
**Full reference:** `CLAUDE.md` and `AGENTS.md` in that folder.

---

## Normal pipeline run (new source file)

Drop a `YYYY-MM-DD_description.txt` (or `.m4a`) into `video-content\Pending\`, then:

```powershell
Set-Location "C:\Users\Leo\clients\leo-content\scripts"
python video_pipeline.py --source "YYYY-MM-DD_description"
```

This runs all phases: HappyScribe transcription → Claude content → JSON2Video render (Pexels + ElevenLabs) → Remotion text polish → post images → Asana tasks.

---

## Re-render existing source (full pipeline)

```powershell
python video_pipeline.py --source "YYYY-MM-DD_description" --force-rerender
```

---

## Remotion-only re-render (when JSON2Video MP4s already exist)

Use when `video_0X.mp4` exist but `remotion_0X.mp4` are missing — skips JSON2Video to avoid re-spending credits.
**Symptom:** Text appears at the bottom of the video instead of centered.

```powershell
# Step 1 — render
$stem = "YYYY-MM-DD_description"   # exact folder/file stem
$contentFile = "C:\Users\Leo\clients\leo-content\video-content\output\$stem\${stem}_content.json"
Set-Location "C:\Users\Leo\clients\leo-content\remotion-video-workflow\remotion-video-generator"
npm run render:source -- --source $contentFile --count 3

# Step 2 — copy outputs to source folder
$remotionOut = "C:\Users\Leo\clients\leo-content\remotion-video-workflow\output\remotion"
$dest = "C:\Users\Leo\clients\leo-content\video-content\output\$stem"
foreach ($i in 1..3) {
    $idx = $i.ToString().PadLeft(2,'0')
    Copy-Item "$remotionOut\${stem}_remotion_${idx}.mp4" "$dest\" -Force -ErrorAction SilentlyContinue
    Copy-Item "$remotionOut\${stem}_remotion_${idx}_caption.txt" "$dest\" -Force -ErrorAction SilentlyContinue
}
```

Takes ~8–12 min per video. Requires ffmpeg (for audio extraction) and Node/npm.

---

## Expected output files (per source)

| File | Description |
|---|---|
| `{stem}_video_01.mp4` | JSON2Video bootstrap (text at bottom — not for review) |
| `{stem}_remotion_01.mp4` | **Review-ready** — Pexels BG + ElevenLabs voice + centered DT text |
| `{stem}_remotion_01_caption.txt` | Caption/description for posting |
| `{stem}_video_01_video_script.json` | 5-scene script (hook/problem/lesson/example/cta) |
| `{stem}_video_01_json2video_spec.json` | Full JSON2Video spec (has Pexels URLs Remotion reuses) |
| `{stem}_posts.txt` | All FB + LinkedIn posts ready to copy-paste |
| `{stem}_images\fb_post_01.png` | Facebook/Instagram post image |
| `{stem}_images\li_post_01.png` | LinkedIn post image |

---

## Key flags

| Flag | Effect |
|---|---|
| `--dry-run` | Generate scripts/spec, skip render + Asana |
| `--force-rerender` | Re-render even if MP4 exists |
| `--skip-remotion` | Stop after JSON2Video (debug only) |
| `--json2video-visual-mode pexels` | Explicit Pexels mode (default) |
| `--post-image-source pexels` | Pexels stock photo for post images (default) |
| `--topic-hint "..."` | Force a specific angle for the video script |
| `--video-index N` | Use Nth video concept only |

---

## Remotion text style rules

- Centered in frame — never bottom-anchored
- Colors: `#40D6E3` aqua, `#5F6164` graphite, `#000000` black, `#FFFFFF` white
- No logo, wordmark, `DigitalTrack`, or handle in any Remotion output
- Overlay text must be short standalone labels readable without audio
  - Good: `"Referrals are not a system"`
  - Too long: `"You cannot rely on word of mouth forever because the market changes"`

---

## Secrets required

All in `C:\Users\Leo\clients\.secrets\`:
`anthropic_key.txt`, `json2video_key.txt`, `pexels_api_key.txt`, `elevenlabs_voice_id.txt`, `json2video_elevenlabs_connection.txt`, `happyscribe_api_key.txt`, `asana_token.txt`
