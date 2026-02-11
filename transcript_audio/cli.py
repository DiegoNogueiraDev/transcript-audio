import argparse
import sys
import os

from transcript_audio.transcriber import (
    transcribe,
    to_srt,
    to_vtt,
    to_txt,
    AVAILABLE_MODELS,
    format_timestamp,
)


def main():
    parser = argparse.ArgumentParser(
        prog="transcript-audio",
        description="Transcribe audio files using OpenAI Whisper.",
    )
    parser.add_argument("file", help="Path to the audio file")
    parser.add_argument(
        "-m", "--model",
        default="turbo",
        choices=AVAILABLE_MODELS,
        help="Whisper model (default: turbo)",
    )
    parser.add_argument(
        "-l", "--language",
        default=None,
        help="Language code (e.g. pt, en). Auto-detect if omitted.",
    )
    parser.add_argument(
        "-f", "--format",
        default="txt",
        choices=["txt", "srt", "vtt", "plain"],
        help="Output format (default: txt)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output file path. Prints to stdout if omitted.",
    )

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    def progress(msg):
        print(f"  {msg}", file=sys.stderr)

    result = transcribe(
        file_path=args.file,
        model_name=args.model,
        language=args.language,
        progress_callback=progress,
    )

    print(
        f"\n  Language: {result['language']} | "
        f"Duration: {format_timestamp(result['duration'])}",
        file=sys.stderr,
    )

    if args.format == "srt":
        content = to_srt(result["segments"])
    elif args.format == "vtt":
        content = to_vtt(result["segments"])
    elif args.format == "plain":
        content = result["text"]
    else:
        content = to_txt(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n  Saved to: {args.output}", file=sys.stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
