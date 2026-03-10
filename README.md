# 🌍 LinguaCoach

> **A language corrector that teaches instead of just fixing.**  
> Write in any language you're learning — LinguaCoach corrects every mistake and explains *why* in your native language.

---

## ✨ What It Does

Most language tools give you the corrected text and move on. LinguaCoach works differently: it breaks down **every single error** with a grammatical explanation in Portuguese, so you actually understand what went wrong and why.

Write your Spanish homework, your French journal entry, or a practice paragraph in German — and get back:

- 📋 A list of every error, with the original and corrected snippet side by side
- 💡 A plain-language grammatical explanation for each mistake
- ✅ The full corrected version of your text
- 🗣️ A natural, native-speaker rewrite
- 📊 An estimated CEFR proficiency level (A1 → C2)
- 🧠 A session-wide error pattern panel showing which mistakes you repeat most

---

## 🖼️ Screenshots

> _Add screenshots here after running the app locally._  
> Suggested shots: the main form, an error card expanded, and the error pattern panel.

---

## 🏗️ Architecture

```
User text + target language
        │
        ▼
   Streamlit UI  (app.py)
        │
        ▼
  correct_text()  (ai_corrector.py)
        │  builds structured prompt
        ▼
    Gemini API
        │  returns strict JSON
        ▼
  json.loads() → Python dict
        │
        ▼
  Streamlit renders:
    • error expanders (colored)
    • corrected text
    • natural version
    • CEFR level
    • session error patterns
```

---

## 🗂️ Project Structure

```
linguacoach/
├── app.py            # Streamlit UI — all rendering logic
├── ai_corrector.py   # AI layer — prompt, API call, JSON parsing
├── requirements.txt  # Python dependencies
├── .env              # Your API key
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/JoaoHPS06/Linguacoach.git
cd Linguacoach
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

> You can get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com).

### 5. Run the app

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 🧠 How the AI Prompt Works

The core of LinguaCoach is its system prompt. It instructs the model to:

- Act as a polyglot language teacher, not an autocorrect tool
- Return **only raw JSON** — no markdown, no extra text
- Explain every error in Portuguese, referencing the grammatical rule
- Estimate the user's CEFR level based on the errors found

The JSON schema returned by the model:

```json
{
  "errors": [
    {
      "trecho_original": "the original wrong snippet",
      "trecho_corrigido": "the corrected snippet",
      "tipo_erro": "error type (e.g. verb tense, agreement)",
      "explicacao_pt": "grammatical explanation in Portuguese"
    }
  ],
  "corrected_text": "full corrected version of the text",
  "natural_version": "how a native speaker would actually write it",
  "overall_level": "estimated CEFR level (A1–C2)"
}
```

---

## 💡 Real-World Usage Tip

Instead of writing your language practice exercises in Google Docs, write them directly in LinguaCoach. You'll learn from your mistakes in real time instead of just seeing the right answer.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| AI Model | [Gemini 2.5 Flash](https://aistudio.google.com) via `google-genai` |
| Environment | `python-dotenv` |
| Language | Python 3.10+ |

---

## 📄 License

MIT License. Feel free to fork, extend, and build on this project.
