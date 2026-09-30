# 🌐 Language Translation Tool


A web app where you type text, pick source and target languages, and get the translation instantly.

## Features
- Text box with character counter (5000 char limit)
- Source language (with **auto-detect**) and target language selection
- Swap-languages button
- Clear translation output with a **copy button** (top-right of the result box)
- **Text-to-speech** playback of the translated text
- Error handling (empty input, no internet, unsupported TTS language)

## Tech Stack
- Python 3.9+
- [Streamlit](https://streamlit.io/) – user interface
- [deep-translator](https://pypi.org/project/deep-translator/) – Google Translate access (no API key needed)
- [gTTS](https://pypi.org/project/gTTS/) – text-to-speech

## Setup & Run
```bash
git clone https://github.com/<your-username>/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://localhost:8501. An internet connection is required.

## Using an official paid API instead
`deep-translator` also ships other translators. To use Microsoft Translator, replace the
`GoogleTranslator(...)` call in `translate_text()` with
`MicrosoftTranslator(api_key="YOUR_KEY", source=source, target=target)`
(imported from `deep_translator`). Never commit API keys to GitHub – use environment variables.

## How it works
1. User enters text and chooses languages.
2. The text is sent to the translation service.
3. The translated response is displayed and stored in `st.session_state` so it stays visible.
4. Optionally, gTTS converts the translation to MP3 and plays it in the browser.

## Author
Your Name –Kalyani jadhav
