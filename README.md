# Claude Voice JP - Bilingual TTS Setup

## What This Is

Modified version of the Claude Code **[voice plugin](https://pchalasani.github.io/claude-code-tools/plugins-detail/voice/)** (`cctools-plugins/voice v1.10.4`) to support both English and Japanese text-to-speech.

| Language | Engine | Port | Voice Default | How It Runs |
|----------|--------|------|---------------|-------------|
| English | pocket-tts | 8000 | `azelma` | `uvx pocket-tts serve` (auto) |
| Japanese | Kokoro-FastAPI | 8880 | `jf_alpha` | Docker container (auto) |

The `say` script detects Japanese characters (hiragana, katakana, kanji) and routes to the appropriate backend. Both servers start automatically if not running.

## Files

- **`say-kokoro`** — Backup of the modified `say` script. The live copy lives at:
  `~/.claude/plugins/cache/cctools-plugins/voice/1.10.4/scripts/say`
- **`~/.claude/voice.local.md`** — Voice config with `voice` (English) and `voice_ja` (Japanese)

## Prerequisites

- `uv` installed (for pocket-tts via `uvx`)
- Docker Desktop installed and running (for Kokoro-FastAPI)

## Installation Steps

1. Install the [voice plugin](https://pchalasani.github.io/claude-code-tools/plugins-detail/voice/) and note the installed version (e.g. `1.10.4`)
2. Copy the modified `say` script over the plugin's default one:
   ```bash
   cp ~/work/claude-voice-jp/say-kokoro ~/.claude/plugins/cache/cctools-plugins/voice/<VERSION>/scripts/say
   ```
3. Copy the voice config:
   ```bash
   cp ~/work/claude-voice-jp/voice.local.md ~/.claude/voice.local.md
   ```

> **Note:** After a plugin update, repeat step 2 with the new version number.

## Available Japanese Voices

| Voice ID | Name | Gender |
|----------|------|--------|
| `jf_alpha` | Alpha | Female |
| `jf_gongitsune` | Gongitsune | Female |
| `jf_nezumi` | Nezumi | Female |
| `jf_tebukuro` | Tebukuro | Female |
| `jm_kumo` | Kumo | Male |

## Available English Voices (Kokoro)

`af_bella`, `af_heart`, `af_nova`, `af_sky`, `am_adam`, `am_echo`, `am_michael`, etc.

(pocket-tts has its own voice set: `azelma`, `alba`, `azure`, etc.)

## Manual Testing

```bash
# Check Kokoro is running
curl http://localhost:8880/v1/audio/voices

# Test Japanese TTS
curl -s -X POST http://localhost:8880/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input":"こんにちは","voice":"jf_alpha","model":"kokoro","response_format":"wav"}' \
  -o test.wav && afplay test.wav

# Test English TTS (pocket-tts)
curl -s -X POST http://localhost:8000/tts \
  -F "text=Hello world" -F "voice_url=azelma" \
  -o test.wav && afplay test.wav
```

## Docker Commands

```bash
# Start Kokoro manually
docker run --rm -d -p 8880:8880 --name kokoro-tts ghcr.io/remsky/kokoro-fastapi-cpu:latest

# Stop Kokoro
docker stop kokoro-tts

# Check logs
docker logs kokoro-tts
```
