# app/ai.py

import os
import json
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def generate_conclusions(chart_type, df_chart, extra_info=None):
    """
    Llama a la API de OpenAI y genera conclusiones en formato HTML.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "<p>Error: No se encontró la OPENAI_API_KEY en el entorno.</p>"

    model = "gpt-4o"

    df_summary = summarize_df(df_chart)
    user_content = build_user_prompt(chart_type, df_summary, extra_info)

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in football analysis. Provides short and concise conclusions."},
            {"role": "user", "content": user_content}
        ],
        "max_tokens": 300,
        "temperature": 0.75
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        message = result["choices"][0]["message"]["content"].strip()
        conclusiones = parse_bullet_points(message)
        # Devolver las conclusiones envueltas en <ul> y <li>
        return "<ul>" + "".join([f"<li>{c}</li>" for c in conclusiones]) + "</ul>"
    else:
        return f"<p>Error: {response.status_code} - {response.text}</p>"
    
def summarize_df(df_chart):
    """
    Crear un breve resumen del df que se usa en la gráfica.
    """
    if df_chart is None or df_chart.empty:
        return "El DataFrame está vacío o no se proporcionó."

    info = []
    info.append(f"- Filas: {len(df_chart)}")
    info.append(f"- Columnas: {list(df_chart.columns)}")

    # Por ejemplo, si 'elo' está presente:
    if 'elo' in df_chart.columns:
        elo_mean = df_chart['elo'].mean()
        info.append(f"- ELO promedio: {elo_mean:.2f}")

    # Podrías extraer más estadísticas, top 3 equipos, etc.
    summary_text = "Resumen del DataFrame:\n" + "\n".join(info)
    return summary_text

def build_user_prompt(chart_type, df_summary, extra_info):
    """
    Construye el texto que se enviará en 'role=user'. Se adapta al idioma.
    """
    if extra_info is None:
        extra_info = {}

    # Determinar el idioma; por defecto, español ("es")

    intro = "Below are the processed (and filtered) data used in the chart:"
    bullet_instruction = "Generate 5 bullet point conclusions (short and concise) discussing the league or the teams in the dataframe."

    lines = [
        intro,
        df_summary,
        "",
        bullet_instruction
    ]

    if chart_type == "bar_chart":
        country = extra_info.get("country", "")
        lines.append(f"Chart Type: Bar Chart (Top 5) - Country: {country}.")
    elif chart_type == "ranking_chart":
        country = extra_info.get("country", "")
        if language == "en":
            lines.append(f"Chart Type: Ranking Evolution (Top 5) - Country: {country}.")
        else:
            lines.append(f"Tipo de gráfico: Evolución de Ranking (Top 5) - País: {country}.")
    elif chart_type == "violin_plot":
        lines.append("Chart Type: Violin Plot (ELO vs country).")
    elif chart_type == "heatmap":
        lines.append("Chart Type: Heatmap (Club vs. Year).")
    elif chart_type == "team_trend_chart":
        team = extra_info.get("team", "")
        lines.append(f"Chart Type: ELO Trend for a specific team. Team: {team}.")
    else:
        lines.append(f"Chart Type: {chart_type} (unknown).")

    return "\n".join(lines)

def parse_bullet_points(text):
    """
    Separa el texto en líneas y limpia números o guiones al inicio.
    Además, reemplaza delimitadores ** con etiquetas <strong>.
    """
    lines = text.split("\n")
    conclusiones = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Eliminar "1.", "1)", "-", etc.
        line = line.lstrip("0123456789.-) ")
        if line:
            # Reemplazar correctamente **texto** con <strong>texto</strong>
            line = line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            conclusiones.append(line.strip())
    return conclusiones