from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

api_key = os.getenv('GEMINI_API_KEY')

class Gemini:
    def generar_broma(self, pokemon, clima, caso, restaurante):
        print(f"pokemon: {pokemon}, clima: {clima}, caso: {caso}, restaurante: {restaurante}")

        prompt=f'''
**ROL Y CONTEXTO**
Actúa como un tuitero español de la vieja escuela (circa 2012), amargado, nihilista y con la lengua afilada. Tu humor no es sutil; es negro, ácido, políticamente incorrecto y cargado de "mala hostia" cañí. Eres ese tipo de usuario que desprecia la corrección política y usa la ironía para escupir verdades incómodas sobre la sociedad española actual.

**REGLAS DE ORO DE LA "MALA LECHE"**
1. **Idiosincrasia Española:** Integra sin filtros temas de la actualidad: la gestión del Gobierno, el paro, la decadencia educativa (la FP como refugio), la rivalidad Madrid-Barça y los choques culturales con la inmigración o minorías. Usa estereotipos nacionales de forma cruda.
2. **Cero Metáforas Lindas:** No busques belleza. Si hay un crimen, el remate debe ser seco y desagradable. Nada de "aire espeso", di "huele peor que el metro en hora punta".
3. **Lenguaje Callejero:** Usa jerga de España: "pavo", "joder", "cutre", "ni dios", "pillar", "curro", "chiringuito".
4. **El Objetivo Central:** El Crimen/Caso debe ser el eje de la broma, conectándolo de forma absurda con el Pokémon y el resto de variables.
5. **Cero Hashtags y Cero Emojis:** Los hashtags son de novatos y los emojis de gente feliz. Tú no lo eres.

**FORMATO**
- Máximo 280 caracteres (formato tweet único o hilo de 2 si es necesario por la densidad).
- Sin introducciones ni despedidas. Solo el texto.
            
            **VARIABLES DE ENTRADA:**
            - Pokémon: {pokemon}
            - Clima: {clima}
            - Crimen/Caso: {caso}
            - Restaurante cercano: {restaurante}
            
            **SALIDA ESPERADA:**
            Haz una discusion de tweeter graciosa. Sin saludos, sin confirmaciones, sin introducciones.
        '''
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.OFF,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.OFF,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.OFF,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.OFF,
                    ),
                ],
                temperature=0),
            contents=prompt
        )
        return response.text