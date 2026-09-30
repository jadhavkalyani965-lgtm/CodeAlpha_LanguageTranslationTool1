"""
CodeAlpha AI Internship - Task 1: Language Translation Tool
------------------------------------------------------------
A Streamlit web app that translates text between languages using
Google Translate (through the `deep-translator` library, which needs no
paid API key).

Features
  * Text input + source / target language selection (with auto-detect)
  * Swap languages button
  * Translated text shown clearly, with a built-in copy button
  * Text-to-speech (gTTS) for the translated text
  * Character counter and friendly error handling

Run:  streamlit run app.py
"""

import io
import time
from deep_translator.exceptions import TooManyRequests
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

MAX_CHARS = 5000  # Google Translate limit per request

# Fallback list used if the supported-language lookup fails (e.g. offline).
FALLBACK_LANGUAGES = {
    "english": "en", "hindi": "hi", "marathi": "mr", "gujarati": "gu",
    "bengali": "bn", "tamil": "ta", "telugu": "te", "urdu": "ur",
    "french": "fr", "german": "de", "spanish": "es", "italian": "it",
    "portuguese": "pt", "russian": "ru", "japanese": "ja", "korean": "ko",
    "chinese (simplified)": "zh-CN", "arabic": "ar",
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_languages() -> dict:
    """Return {'language name': 'code'} sorted alphabetically."""
    try:
        langs = GoogleTranslator().get_supported_languages(as_dict=True)
    except Exception:
        langs = FALLBACK_LANGUAGES
    return dict(sorted(langs.items()))

def translate_text(text: str, source: str, target: str, retries: int = 3) -> str:
    """Call the translation API, retrying if Google rate-limits us."""
    for attempt in range(retries):
        try:
            return GoogleTranslator(source=source, target=target).translate(text)
        except TooManyRequests:
            if attempt == retries - 1:
                raise
            time.sleep(2 * (attempt + 1))  # wait 2s, then 4s, then give up


def text_to_speech(text: str, lang_code: str) -> bytes:
    """Convert text to MP3 bytes using gTTS."""
    audio_buffer = io.BytesIO()
    gTTS(text=text, lang=lang_code).write_to_fp(audio_buffer)
    return audio_buffer.getvalue()


def swap_languages() -> None:
    """Swap source and target (callback for the swap button)."""
    src, tgt = st.session_state.src_lang, st.session_state.tgt_lang
    if src == "auto detect":
        st.warning("Cannot swap when the source is 'auto detect'.")
        return
    st.session_state.src_lang, st.session_state.tgt_lang = tgt, src


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------
st.set_page_config(page_title="Language Translation Tool", page_icon="🌐")
st.title("🌐 Language Translation Tool")
st.caption("CodeAlpha AI Internship - Task 1")

languages = get_languages()
source_options = ["auto detect"] + list(languages.keys())
target_options = list(languages.keys())

# Default selections
st.session_state.setdefault("src_lang", "auto detect")
st.session_state.setdefault("tgt_lang", "hindi" if "hindi" in languages else target_options[0])

col1, col_swap, col2 = st.columns([5, 1, 5])
with col1:
    st.selectbox("From", source_options, key="src_lang")
with col_swap:
    st.write("")  # vertical alignment
    st.write("")
    st.button("⇄", on_click=swap_languages, help="Swap languages")
with col2:
    st.selectbox("To", target_options, key="tgt_lang")

input_text = st.text_area(
    "Enter text",
    height=180,
    max_chars=MAX_CHARS,
    placeholder="Type or paste the text you want to translate...",
)
st.caption(f"{len(input_text)} / {MAX_CHARS} characters")

if st.button("Translate", type="primary"):
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    elif st.session_state.src_lang == st.session_state.tgt_lang:
        st.info("Source and target languages are the same.")
    else:
        source_code = "auto" if st.session_state.src_lang == "auto detect" \
            else languages[st.session_state.src_lang]
        target_code = languages[st.session_state.tgt_lang]
        try:
            with st.spinner("Translating..."):
                result = translate_text(input_text, source_code, target_code)
            st.session_state.result = result
            st.session_state.result_lang = target_code
            st.session_state.audio = None  # reset old audio
        except Exception as exc:
            st.error(f"Translation failed: {exc}")
            st.session_state.result = None

# Show the result (kept in session_state so it survives reruns)
if st.session_state.get("result"):
    st.subheader("Translation")
    # st.code has a built-in copy icon at the top-right -> our "copy button"
    st.code(st.session_state.result, language=None, wrap_lines=True)

    if st.button("🔊 Listen"):
        try:
            with st.spinner("Generating audio..."):
                st.session_state.audio = text_to_speech(
                    st.session_state.result, st.session_state.result_lang
                )
        except Exception as exc:
            st.error(f"Text-to-speech is not available for this language: {exc}")

    if st.session_state.get("audio"):
        st.audio(st.session_state.audio, format="audio/mp3")
