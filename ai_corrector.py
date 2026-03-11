import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


# Initialize the Gemini client using the API key from environment
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# AI Model used
MODEL = "gemini-2.5-flash"


# System prompt instructs the model to act as a language teacher
# and return ONLY a strict JSON — no extra text, no markdown fences
SYSTEM_PROMPT = """Seja um professor de idiomas poliglota em que vai receber um texto e vai 
    corrigi - lo baseado na gramática da linguagem escolhida. Retorne APENAS o JSON, 
    sem nenhum texto antes ou depois no seguinte formato: {
        "errors": [
            {
            "trecho_original": "...",
            "trecho_corrigido": "...",
            "tipo_erro": "...",
            "explicacao_pt": "..."
            }
        ],
        "corrected_text": "...",
        "natural_version": "...",
        "overall_level": "..."
        }"""


def correct_text(text, target_language, native_language="português"):
    """
    Sends the user's text to the AI model for grammar correction and pedagogical analysis.

    Args:
        text: The raw text written by the user.
        target_language: The language the user is practicing (e.g., "Spanish").
        native_language: The user's native language, used for explanations. Defaults to "Portuguese".

    Returns:
        A dictionary with keys: errors, corrected_text, natural_version, overall_level.
        Returns an error dict if the AI response cannot be parsed.
    """
    # User message combines the target language, native language, and the actual text
    user_message = f"Corrija o seguinte texto em {target_language}, escrito por um falante de {native_language}: {text}"

    # Call the Gemini API with the system instruction and user message
    response = client.models.generate_content(
        model=MODEL,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json"
        )
    )

    return _parse_json_response(response.text)


def transcribe_audio(audio_bytes, target_language):
    """
    Transcribes an audio recording without applying grammar correction.

    Args:
        audio_bytes: The raw audio content in bytes (WAV format).
        target_language: The language spoken in the audio (e.g., "Inglês").

    Returns:
        A string with the exact transcribed text, as returned by the model.
    """
    # Prompt explicitly asks for transcription only — no corrections or commentary
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            f"Transcreva exatamente o que foi dito neste áudio em {target_language}. Retorne APENAS o texto transcrito, sem comentários.",
            types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
        ]
    )
    return response.text.strip()


def _parse_json_response(raw_text: str) -> dict:
    # Parses JSON from model response.
    try:
        return json.loads(raw_text.strip())
    except json.JSONDecodeError:
        return {"erro": "Não foi possível interpretar a resposta da IA."}
