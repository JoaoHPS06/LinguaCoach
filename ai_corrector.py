import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini client using the API key from environment
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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
def correct_text(text, target_language, native_language="português"):
    # System prompt instructs the model to act as a language teacher
    # and return ONLY a strict JSON — no extra text, no markdown fences
    system_prompt = """Seja um professor de idiomas poliglota em que vai receber um texto e vai 
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
    
    # User message combines the target language, native language, and the actual text
    user_message = f"Corrija o seguinte texto em {target_language}, escrito por um falante de {native_language}: {text}"

    # Call the Gemini API with the system instruction and user message
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )

    # Strip markdown code fences if the model wraps the JSON anyway
    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]  # grab content between fences
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]          # remove the "json" language tag
    raw_text = raw_text.strip()

    # Parse JSON and return as a Python dict
    try:
        resultado = json.loads(raw_text)
    except json.JSONDecodeError:
        # Return a safe fallback if the AI response is malformed
        resultado = {"erro": "Não foi possível interpretar a resposta da IA."}
        
    return resultado


