import gradio as gr
from inference_file import inference

MAX_SIZE_MB = "50"
MAX_SECONDS = 60


def transcribe_audio(audio_file):

    if audio_file is None or (isinstance(audio_file, str) and audio_file.strip() == ""):
        return "⚠️ Please upload an audio file first. If using the recorder press the stop button first."

    if isinstance(audio_file, str):
        import soundfile as sf

        info = sf.info(audio_file)
        if info.duration > MAX_SECONDS:
            return f"❌ Audio too long ({info.duration:.1f}s). Please upload audio shorter than {MAX_SECONDS} seconds."

    try:
        return inference(audio_file)

    except Exception as e:
        return f"❌ Error during transcription: {str(e)}"


# Build Gradio UI
with gr.Blocks(
    title="🎙️ Mmeslay",
    theme=gr.themes.Soft(),
) as demo:
    gr.Markdown(
        """
        # 🎙️  Mmeslay by G1ya777 (https://github.com/G1ya777/Mmeslay) 🎙️
        Upload an audio file or record from your microphone to get a transcription.
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            audio_input = gr.Audio(
                label="Upload Audio File",
                type="filepath",
                sources=["upload", "microphone"],
                format="mp3",
            )
            transcribe_btn = gr.Button("🚀 Transcribe", variant="primary", size="lg")

        with gr.Column(scale=2):
            text_output = gr.Textbox(
                label="Transcription",
                placeholder="Transcription will appear here...",
                lines=10,
                buttons=["copy"],
            )

    transcribe_btn.click(
        fn=transcribe_audio,
        inputs=audio_input,
        outputs=text_output,
    )

    gr.Examples(
        examples=[
            "ressources/examples/e1.mp3",
            "ressources/examples/e2.mp3",
            "ressources/examples/e3.mp3",
        ],
        inputs=audio_input,
    )
    gr.Markdown(
        """
    ---
    **Example Audio Credits**
    | File | Author / Source | License |
    |------|----------------|---------|
    | e1.mp3 | samir_t, [Source](https://tatoeba.org/en/sentences/show/9678657) | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/fr/) |
    | e2.mp3 | Selyan, [Source](https://tatoeba.org/en/sentences/show/11313226) | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/fr/) |
    | e2.mp3 | BouazizAitD, [Source](https://tatoeba.org/en/sentences/show/11718739) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

    """
    )


if __name__ == "__main__":
    demo.launch(
        max_file_size=MAX_SIZE_MB + "mb",
    )
