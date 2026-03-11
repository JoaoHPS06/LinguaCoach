import streamlit as st
from ai_corrector import correct_text, transcribe_audio
from collections import Counter


# --- Input Components ---
def read_text():
    """Renders a text area for the user to input the text they want corrected."""
    return st.text_area("Escreva o texto que você quer corrigir:", key="user_text")


def select_language():
    """Renders a dropdown for the user to select the target language."""
    return st.selectbox("Idioma Alvo:", ("Inglês", "Espanhol", "Francês", "Alemão"),
                        key="target_language")


# --- Result Rendering ---
def render_errors(errors):
    """Renders each grammar error inside an expandable card with colored feedback."""
    st.subheader("📋 Erros Encontrados")

    if not errors:
        st.success("✅ **Parabéns!** Seu texto não contém erros.")
        return

    for error in errors:
        # Each expander shows a quick summary: original → corrected
        with st.expander(f"❌ {error['trecho_original']} → ✅ {error['trecho_corrigido']}"):
            st.markdown(f"🔴 **Original:** {error['trecho_original']}")
            st.markdown(f"🟢 **Corrigido:** {error['trecho_corrigido']}")
            st.markdown(f"📌 **Tipo:** {error['tipo_erro']}")
            st.markdown(f"💡 **Explicação:** {error['explicacao_pt']}")


def render_corrected_text(corrected_text):
    """Renders the full corrected version of the text."""
    st.subheader("✅ Texto Corrigido")
    st.write(corrected_text)


def render_natural_version(natural_version):
    """Renders the natural, native-speaker version of the text."""
    st.subheader("🗣️ Como um nativo diria")
    st.write(natural_version)


def render_level(overall_level):
    """Renders the estimated CEFR proficiency level."""
    st.info(f"📊 Nível Estimado: **{overall_level}**")


def render_results(result):
    """Renders the full correction output: errors, corrected text, natural version, and level."""
    render_errors(result.get("errors", []))
    render_corrected_text(result.get("corrected_text", ""))
    render_natural_version(result.get("natural_version", ""))
    render_level(result.get("overall_level", "N/A"))


def render_error_patterns(history):
    """Renders a summary panel showing the most frequent error types across the session."""
    if not history:
        return

    st.divider()
    st.subheader("📊 Seus Padrões de Erros")
    st.caption("Tipos de erros acumulados durante a sessão.")

    count = Counter(history)
    for error_type, quantity in count.most_common():
        st.write(f"**{error_type}** — {quantity}x")


# --- Mode Handlers ---
def handle_audio_mode(language):
    """Handles audio recording, transcription, and editable text area for speech mode."""
    audio = st.audio_input("🎙️ Grave sua fala:")

    if audio is not None:
        audio_bytes = audio.getvalue()
        audio_hash = hash(audio_bytes)

        # Only re-transcribe if the audio has changed
        if st.session_state.get("audio_hash") != audio_hash:
            with st.spinner("🔤 Transcrevendo automaticamente..."):
                st.session_state.transcricao = transcribe_audio(audio_bytes, language)
                st.session_state.audio_hash = audio_hash
                st.session_state.transcricao_edit = st.session_state.transcricao

    if "transcricao" in st.session_state:
        st.text_area(
            "📝 O que você disse (edite se necessário):",
            key="transcricao_edit"
        )


# --- Main App ---
def main():
    st.title("🌍 LinguaCoach")
    st.caption("Escreva em qualquer língua, aprenda com cada erro!")

    # Initialize session history if it doesn't exist yet
    if "error_history" not in st.session_state:
        st.session_state.error_history = []

    modo = st.radio("Modo:", ["✍️ Texto", "🎤 Fala"], horizontal=True)
    language = select_language()

    if modo == "🎤 Fala":
        handle_audio_mode(language)

    # Form groups text input + submit button together
    with st.form("linguacoach_form"):
        if modo == "✍️ Texto":
            text = read_text()
        submitted = st.form_submit_button("✏️ Corrija e Aprenda")

    if submitted:
        with st.spinner("🔍 Analisando..."):
            if modo == "🎤 Fala":
                if "transcricao" not in st.session_state:
                    st.warning("⚠️ Grave e transcreva o áudio antes de continuar!")
                    st.stop()
                result = correct_text(st.session_state.transcricao_edit, language)
            else:
                result = correct_text(text, language)

        render_results(result)

        for error in result.get("errors", []):
            st.session_state.error_history.append(error["tipo_erro"])

    # Always show the error pattern panel if there's session data
    render_error_patterns(st.session_state.error_history)


if __name__ == "__main__":
    main()
