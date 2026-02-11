# Transcript Audio

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-green.svg)](https://github.com/openai/whisper)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io)

Audio transcription tool powered by [OpenAI Whisper](https://github.com/openai/whisper). Supports any audio length with high precision. Available as both a **web interface** (Streamlit) and a **CLI**.

---

## Features

- **High-precision transcription** using OpenAI Whisper models
- **Web interface** with Streamlit for easy drag-and-drop usage
- **CLI** for scripting and automation
- **Multiple output formats:** TXT (with timestamps), SRT, VTT, plain text
- **Auto language detection** or manual selection (10+ languages)
- **12+ audio/video formats** supported
- **Word-level timestamps** for precise alignment
- **Download** transcriptions directly from the web interface

## Requirements

- **Python 3.10+**
- **FFmpeg** installed on your system

### Installing FFmpeg

<details>
<summary>Ubuntu / Debian</summary>

```bash
sudo apt install ffmpeg
```
</details>

<details>
<summary>Fedora</summary>

```bash
sudo dnf install ffmpeg
```
</details>

<details>
<summary>macOS (Homebrew)</summary>

```bash
brew install ffmpeg
```
</details>

<details>
<summary>Windows (Chocolatey)</summary>

```bash
choco install ffmpeg
```
</details>

## Installation

```bash
git clone https://github.com/DiegoNogueiraDev/transcript-audio.git
cd transcript-audio
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
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

# Export as VTT (web subtitles)
python -m transcript_audio.cli audio.mp3 -f vtt -o subtitles.vtt

# Plain text (no timestamps)
python -m transcript_audio.cli audio.mp3 -f plain
```

#### CLI Options

| Option | Description | Default |
|---|---|---|
| `file` | Path to the audio file | *required* |
| `-m, --model` | Whisper model (`tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3`, `turbo`) | `turbo` |
| `-l, --language` | Language code (`pt`, `en`, `es`, `fr`, `de`, etc.). Auto-detects if omitted | `auto` |
| `-f, --format` | Output format: `txt`, `srt`, `vtt`, `plain` | `txt` |
| `-o, --output` | Save to file instead of printing to stdout | `stdout` |

## Models

| Model | Parameters | Disk Size | Speed | Precision |
|---|---|---|---|---|
| `tiny` | 39M | ~75 MB | Fastest | Low |
| `base` | 74M | ~142 MB | Fast | Fair |
| `small` | 244M | ~466 MB | Moderate | Good |
| `medium` | 769M | ~1.5 GB | Slow | High |
| `large-v2` | 1550M | ~2.9 GB | Slowest | Very High |
| `large-v3` | 1550M | ~2.9 GB | Slowest | Highest |
| `turbo` | 809M | ~1.5 GB | Fast | High |

> **Recommendation:** Use `turbo` for the best speed/quality tradeoff. Use `large-v3` when maximum precision is required.

## Supported Formats

| Audio | Video |
|---|---|
| MP3, WAV, M4A, FLAC, OGG, WMA, AAC, OPUS | MP4, MKV, AVI, WEBM |

## Project Structure

```
transcript-audio/
├── app.py                        # Streamlit web interface
├── transcript_audio/
│   ├── __init__.py
│   ├── transcriber.py            # Core transcription engine
│   └── cli.py                    # Command-line interface
├── requirements.txt
├── LICENSE
└── README.md
```

## Contributing

Contributions are welcome! Please follow the steps below:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/my-feature`)
3. **Commit** your changes (`git commit -m 'Add my feature'`)
4. **Push** to the branch (`git push origin feature/my-feature`)
5. **Open** a Pull Request

### Guidelines

- Follow existing code style and patterns
- Keep changes focused and atomic
- Update documentation if needed
- Test your changes before submitting

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech recognition models
- [Streamlit](https://streamlit.io) for the web framework
- [FFmpeg](https://ffmpeg.org) for audio processing
