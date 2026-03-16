from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

api_key = os.getenv('GEMINI_API_KEY')

class Gemini:
    def generar_broma(self, pokemon, clima, caso, restaurante):
        context ='''
        Actúa como un comediante de humor negro y ácido.
        Usa ironía, sarcasmo y exageración para crear chistes que jueguen con la incomodidad. 
        El humor debe ser oscuro, existencial, absurdo y autocrítico, como si mezclaras humor pesimista con situaciones ridículas en la conyuntura hispana y americana actual y referencias reales. 
        Mantén el tono ingenioso, inesperado y ligeramente cruel.
        Debe ser una broma corta.
        '''
        prompt=f'''
            Genera un texto gracioso con los siguientes elementos: pokemon {pokemon} , clima {clima}, {caso}, {restaurante}.
        '''
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=context,
                temperature=1),
            contents=prompt
        )
        return response.text