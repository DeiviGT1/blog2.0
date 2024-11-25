# app/python/openai/openaiapi.py

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def generar_respuesta(song_name, artista):
    api_key = os.getenv("OPENAI_API_KEY")
    model = "gpt-4o"

    # Construir el prompt
    prompt = (f"Quiero recomendaciones de canciones similares a '{song_name}' de '{artista}'.\n"
              f"Por favor, proporciona una lista numerada de 10 canciones, incluyendo el nombre del artista para cada una.")

    # Configurar la solicitud HTTP
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Datos para la solicitud
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Eres un asistente que proporciona recomendaciones musicales."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.75
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Verificar la respuesta
    if response.status_code == 200:
        result = response.json()
        message = result['choices'][0]['message']['content'].strip()
        song_recommendations = message.split("\n")
        # Procesar y limpiar las recomendaciones
        recomendaciones = []
        for song in song_recommendations:
            song = song.strip()
            if song and (song[0].isdigit() or song.startswith('-')):
                # Eliminar el número o guión al inicio
                song = song.lstrip('0123456789.- ').strip()
                recomendaciones.append(song)
            elif song:
                recomendaciones.append(song.strip())
        recomendaciones = list(set(recomendaciones))  # Eliminar duplicados
        return recomendaciones
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []