# Transcript Audio

Audio transcription tool powered by OpenAI Whisper. Supports any audio length with high precision. Available as both a web interface (Streamlit) and a CLI.

## Requirements

- Python 3.10+
- FFmpeg installed on your system

### Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# macOS
brew install ffmpeg
```

## Installation

```bash
git clone https://github.com/diegonogueira/transcript-audio.git
cd transcript-audio
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Web Interface

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser. Upload an audio file, choose the model and language, and click **Transcribe**.

### CLI

```bash
# Basic transcription (auto-detect language)
python -m transcript_audio.cli audio.mp3

# Specify model and language
python -m transcript_audio.cli audio.mp3 -m large-v3 -l pt

# Export as SRT subtitles
python -m transcript_audio.cli audio.mp3 -f srt -o subtitles.srt

# Export as VTT
python -m transcript_audio.cli audio.mp3 -f vtt -o subtitles.vtt
```

#### CLI Options

| Option | Description |
|---|---|
| `-m, --model` | Whisper model: `tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3`, `turbo` (default: `turbo`) |
| `-l, --language` | Language code (`pt`, `en`, `es`, etc.). Auto-detects if omitted |
| `-f, --format` | Output format: `txt`, `srt`, `vtt`, `plain` (default: `txt`) |
| `-o, --output` | Save to file instead of printing to stdout |

## Models

| Model | Size | Speed | Precision |
|---|---|---|---|
| `tiny` | 39M | Fastest | Low |
| `base` | 74M | Fast | Fair |
| `small` | 244M | Moderate | Good |
| `medium` | 769M | Slow | High |
| `large-v3` | 1550M | Slowest | Highest |
| `turbo` | 809M | Fast | High |

**Recommendation:** Use `turbo` for the best speed/quality tradeoff. Use `large-v3` when maximum precision is required.

## Supported Audio Formats

MP3, WAV, M4A, FLAC, OGG, WMA, AAC, OPUS, WEBM, MP4, MKV, AVI

## License

MIT
