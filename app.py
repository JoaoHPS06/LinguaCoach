import streamlit as st
from ai_corrector import correct_text
from collections import Counter

# --- Input Components ---

def read_text():
    # Renders a text area for the user to input the text they want corrected.
    return st.text_area("Escreva o texto que você quer corrigir:", key="user_text")

def select_language():
    # Renders a dropdown for the user to select the target language.
    return st.selectbox("Idioma Alvo:", ("Inglês", "Espanhol", "Francês", "Alemão"), 
                        key="target_language")

# --- Result Rendering ---

def render_errors(errors):
    """Renders each grammar error inside an expandable card with colored feedback."""
    st.subheader("📋 Erros Encontrados")

    if len(errors) == 0:
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

# --- Main App ---

def main():
    st.title("🌍 LinguaCoach")
    st.caption("Escreva em qualquer língua, aprenda com cada erro!")

    # Initialize session history if it doesn't exist yet
    if "error_history" not in st.session_state:
        st.session_state.error_history = []

    # Form groups language selector + text input + submit button together
    with st.form("linguacoach_form"):
        language = select_language()
        text = read_text()
        submitted = st.form_submit_button("✏️ Corrija e Aprenda")

    if submitted:
        # Call the AI corrector while showing a loading spinner
        with st.spinner("🔍 Analisando seu texto..."):
            result = correct_text(text, language)

        # Render all result sections
        render_errors(result.get("errors", []))
        render_corrected_text(result.get("corrected_text", ""))
        render_natural_version(result.get("natural_version", ""))
        render_level(result.get("overall_level", "N/A"))

        # Accumulate error types into the session history
        for error in result.get("errors", []):
            st.session_state.error_history.append(error["tipo_erro"])

    # Always show the error pattern panel if there's session data
    render_error_patterns(st.session_state.error_history)

if __name__ == "__main__":
    main()
