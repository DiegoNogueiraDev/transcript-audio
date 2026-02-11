import whisper
import os
import tempfile
import subprocess
import json


AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3", "turbo"]

SUPPORTED_FORMATS = [
    ".mp3", ".wav", ".m4a", ".flac", ".ogg", ".wma",
    ".aac", ".opus", ".webm", ".mp4", ".mkv", ".avi",
]


def get_audio_duration(file_path: str) -> float:
    """Return audio duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet", "-print_format", "json",
                "-show_format", file_path,
            ],
            capture_output=True, text=True, check=True,
        )
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except Exception:
        return 0.0


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS,mmm format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    """Convert seconds to HH:MM:SS.mmm format (VTT)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def transcribe(
    file_path: str,
    model_name: str = "turbo",
    language: str | None = None,
    progress_callback=None,
) -> dict:
    """
    Transcribe an audio file using Whisper.

    Args:
        file_path: Path to the audio file.
        model_name: Whisper model name (tiny, base, small, medium, large, large-v3, turbo).
        language: Language code (e.g. 'pt', 'en'). None for auto-detect.
        progress_callback: Optional callback(status_text) for progress updates.

    Returns:
        dict with keys: text, segments, language, duration
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {ext}. Supported: {SUPPORTED_FORMATS}")

    if progress_callback:
        progress_callback(f"Loading model '{model_name}'...")

    model = whisper.load_model(model_name)

    duration = get_audio_duration(file_path)

    if progress_callback:
        duration_str = format_timestamp(duration) if duration else "unknown"
        progress_callback(f"Transcribing audio ({duration_str})...")

    options = {
        "verbose": False,
        "word_timestamps": True,
        "condition_on_previous_text": True,
    }

    if language:
        options["language"] = language

    result = model.transcribe(file_path, **options)

    if progress_callback:
        progress_callback("Transcription complete!")

    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "id": seg["id"],
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        })

    return {
        "text": result["text"].strip(),
        "segments": segments,
        "language": result.get("language", language or "unknown"),
        "duration": duration,
    }


def to_srt(segments: list[dict]) -> str:
    """Convert segments to SRT subtitle format."""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(seg["text"])
        lines.append("")
    return "\n".join(lines)


def to_vtt(segments: list[dict]) -> str:
    """Convert segments to WebVTT subtitle format."""
    lines = ["WEBVTT", ""]
    for i, seg in enumerate(segments, 1):
        start = format_timestamp_vtt(seg["start"])
        end = format_timestamp_vtt(seg["end"])
        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(seg["text"])
        lines.append("")
    return "\n".join(lines)


def to_txt(result: dict) -> str:
    """Convert transcription result to plain text with timestamps."""
    lines = []
    for seg in result["segments"]:
        ts = format_timestamp(seg["start"])
        lines.append(f"[{ts}] {seg['text']}")
    return "\n".join(lines)
