# AI Content Factory

Automated YouTube Shorts pipeline: topic → script → voice → images → subtitles →
timeline → Remotion render → burned subtitles → YouTube metadata → QC.

## Pipeline

| Step | Service | Output (`storage/`) |
|---|---|---|
| 1. Script | Gemini, schema-constrained JSON | `scripts/{id}.json` |
| 2. Voice | edge-tts, with word timings | `voices/{id}.mp3`, `voices/{id}.words.json` |
| 3. Images | Gemini image 9:16, Pollinations fallback, cached | `images/{id}/` |
| 4. Subtitle | Word timings (Whisper only as fallback) | `subtitles/{id}.srt` |
| 5. Timeline | Images synced to when each sentence is spoken | `timeline/{id}.json` |
| 6. Render | Remotion in Docker, Ken Burns motion + crossfades | `videos/{id}.mp4` |
| 7. Final | FFmpeg subtitle burn | `videos/{id}_final.mp4` |
| 8. Metadata | Gemini title, description, tags | `metadata/{id}.json` |
| 9. QC | ffprobe checks (1080x1920, 30 fps, 10-60 s, covers narration) | |

## Setup

```bash
cp .env.example .env            # fill in GEMINI_API_KEY
docker compose up -d            # PostgreSQL + renderer
docker compose exec renderer npm ci
pip install -r requirements.txt
python -m scripts.init_db
```

FFmpeg must be on your PATH. On Windows you can instead put `ffmpeg.exe` and
`ffprobe.exe` in `tools/ffmpeg/` (they are git-ignored) or set `FFMPEG_PATH`
and `FFPROBE_PATH` in `.env`.

Optional: `pip install -r requirements-whisper.txt` to subtitle audio that has
no edge-tts word timings.

## Usage

```bash
python -m scripts.add_topic "Why the Moon is drifting away"   # prints the ID
python -m scripts.pipeline 1                  # finished steps are skipped
python -m scripts.pipeline 1 --from image     # redo images and everything after
python -m scripts.pipeline 1 --force          # redo everything
```

Each step also has its own script in `scripts/` (`generate_script`,
`generate_voice`, `generate_images`, `generate_subtitle`, `generate_video`,
`generate_final_video`, `generate_metadata`, `qc`).

Settings such as language, models, voice and image style live in `.env`;
see `.env.example` and `app/settings.py`.

## Tests

```bash
pip install pytest
python -m pytest
cd renderer && npm run typecheck
```
