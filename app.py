import streamlit as st
import tempfile
import os
import time

from transcript_audio.transcriber import (
    transcribe,
    to_srt,
    to_vtt,
    to_txt,
    AVAILABLE_MODELS,
    SUPPORTED_FORMATS,
    format_timestamp,
)

st.set_page_config(
    page_title="Transcript Audio",
    page_icon="🎙️",
    layout="wide",
)

st.title("Transcript Audio")
st.markdown("Transcription of audio files using OpenAI Whisper with high precision.")

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")

    model_name = st.selectbox(
        "Whisper Model",
        options=AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index("turbo"),
        help="'turbo' is fast and accurate. 'large-v3' has the highest precision but is slower.",
    )

    language = st.selectbox(
        "Language",
        options=[
            ("Auto-detect", None),
            ("Portuguese", "pt"),
            ("English", "en"),
            ("Spanish", "es"),
            ("French", "fr"),
            ("German", "de"),
            ("Italian", "it"),
            ("Japanese", "ja"),
            ("Chinese", "zh"),
            ("Korean", "ko"),
            ("Russian", "ru"),
        ],
        format_func=lambda x: x[0],
        index=0,
    )

    output_format = st.selectbox(
        "Output Format",
        options=["TXT (with timestamps)", "SRT (subtitles)", "VTT (web subtitles)", "Plain text"],
    )

    st.markdown("---")
    st.markdown(
        f"**Supported formats:** {', '.join(SUPPORTED_FORMATS)}"
    )

# --- Main ---
uploaded_file = st.file_uploader(
    "Upload your audio file",
    type=[fmt.lstrip(".") for fmt in SUPPORTED_FORMATS],
)

if uploaded_file is not None:
    st.audio(uploaded_file)

    if st.button("Transcribe", type="primary", use_container_width=True):
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(uploaded_file.name)[1],
        ) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            status = st.empty()
            progress_bar = st.progress(0)

            def update_status(msg):
                status.markdown(f"**{msg}**")

            progress_bar.progress(10)
            start_time = time.time()

            result = transcribe(
                file_path=tmp_path,
                model_name=model_name,
                language=language[1],
                progress_callback=update_status,
            )

            elapsed = time.time() - start_time
            progress_bar.progress(100)

            status.markdown(
                f"**Done!** Transcribed in {elapsed:.1f}s | "
                f"Language: {result['language']} | "
                f"Duration: {format_timestamp(result['duration'])}"
            )

            st.session_state["result"] = result

        finally:
            os.unlink(tmp_path)

if "result" in st.session_state:
    result = st.session_state["result"]

    st.markdown("---")
    st.subheader("Transcription")

    # Display based on format
    if output_format == "Plain text":
        content = result["text"]
    elif output_format == "TXT (with timestamps)":
        content = to_txt(result)
    elif output_format == "SRT (subtitles)":
        content = to_srt(result["segments"])
    else:
        content = to_vtt(result["segments"])

    st.text_area("Result", value=content, height=400)

    # Download button
    ext_map = {
        "TXT (with timestamps)": ".txt",
        "SRT (subtitles)": ".srt",
        "VTT (web subtitles)": ".vtt",
        "Plain text": ".txt",
    }

    st.download_button(
        label="Download transcription",
        data=content,
        file_name=f"transcription{ext_map[output_format]}",
        mime="text/plain",
        use_container_width=True,
    )

    # Segments table
    with st.expander("View segments"):
        for seg in result["segments"]:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.caption(f"{format_timestamp(seg['start'])}")
            with col2:
                st.markdown(seg["text"])
