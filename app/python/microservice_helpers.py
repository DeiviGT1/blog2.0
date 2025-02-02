# app/python/microservice_helpers.py

import requests
import json
import logging
import pandas as pd

# URL base de tu microservicio de graficación en Cloud Run
MICROSERVICE_URL = "https://microservice-plot-163142221066.us-east1.run.app"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_datetime_columns_to_str(df):
    """
    Convierte todas las columnas datetime del DataFrame a strings en formato 'YYYY-MM-DD'.
    """
    df = df.copy()
    datetime_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime']).columns
    for col in datetime_columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d')
    return df

def get_plot_team_trend_chart(df, teams):
    df = convert_datetime_columns_to_str(df)
    payload = {
        "teams": teams,
        "df": df.to_dict(orient="records")
    }
    url = f"{MICROSERVICE_URL}/plot_team_trend"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json().get("image_base64")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en plot_team_trend: {http_err} - Respuesta: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en plot_team_trend: {err}")
    return None

def get_plot_top_teams_country(df, country, num_teams=5):
    """
    Se filtran en el frontend los datos para obtener solo los top num_teams equipos.
    De esta forma, el payload enviado al backend ya no incluye el parámetro num_teams.
    """
    df = convert_datetime_columns_to_str(df)
    if country:
        # Filtrar el DataFrame para el país seleccionado
        df_country = df[df['country'] == country]
        # Calcular el ELO promedio por club
        elo_mean = df_country.groupby('club')['elo'].mean().reset_index()
        # Seleccionar los top num_teams equipos
        top_clubs = elo_mean.sort_values('elo', ascending=False).head(num_teams)['club'].tolist()
        # Filtrar el DataFrame para incluir solo esos equipos
        df_filtered = df_country[df_country['club'].isin(top_clubs)]
    else:
        df_filtered = df

    payload = {
        "country": country,
        "df": df_filtered.to_dict(orient="records")
    }
    url = f"{MICROSERVICE_URL}/plot_top_teams_country"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json().get("image_base64")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en get_plot_top_teams_country: {http_err} - Respuesta: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en get_plot_top_teams_country: {err}")
    return None

def get_plot_ranking_evolution(df, country, num_teams=5):
    """
    Se filtran en el frontend los datos para incluir únicamente los top num_teams equipos del país.
    El payload enviado al backend no incluye el parámetro num_teams.
    """
    df = convert_datetime_columns_to_str(df)
    if country:
        df_country = df[df['country'] == country]
        elo_mean = df_country.groupby('club')['elo'].mean().reset_index()
        top_clubs = elo_mean.sort_values('elo', ascending=False).head(num_teams)['club'].tolist()
        df_filtered = df_country[df_country['club'].isin(top_clubs)]
    else:
        df_filtered = df

    payload = {
        "country": country,
        "df": df_filtered.to_dict(orient="records")
    }
    url = f"{MICROSERVICE_URL}/plot_ranking_evolution"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json().get("image_base64")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en plot_ranking_evolution: {http_err} - Respuesta: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en plot_ranking_evolution: {err}")
    return None

def get_plot_violin_elo(df):
    df = convert_datetime_columns_to_str(df)
    payload = {
        "df": df.to_dict(orient="records")
    }
    url = f"{MICROSERVICE_URL}/plot_violin_elo"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json().get("image_base64")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en plot_violin_elo: {http_err} - Respuesta: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en plot_violin_elo: {err}")
    return None

def get_plot_heatmap_elo(df, num_teams=5):
    df = convert_datetime_columns_to_str(df)
    # Calcular el ELO promedio por club y seleccionar los top num_teams equipos
    elo_mean = df.groupby('club')['elo'].mean().reset_index()
    top_clubs = elo_mean.sort_values('elo', ascending=False).head(num_teams)['club'].tolist()
    # Filtrar el DataFrame para incluir solo esos equipos
    df_filtered = df[df['club'].isin(top_clubs)]
    
    payload = {
        "df": df_filtered.to_dict(orient="records")
    }
    url = f"{MICROSERVICE_URL}/plot_heatmap_elo"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json().get("image_base64")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en plot_heatmap_elo: {http_err} - Respuesta: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en plot_heatmap_elo: {err}")
    return None

def get_ranking_por_pais(df, pais):
    """
    Se filtran en el frontend los datos para obtener, por ejemplo, los top 5 equipos del país.
    """
    df = convert_datetime_columns_to_str(df)
    if pais:
        df_country = df[df['country'] == pais]
        elo_mean = df_country.groupby('club')['elo'].mean().reset_index()
        top_clubs = elo_mean.sort_values('elo', ascending=False).head(5)['club'].tolist()
        df_filtered = df_country[df_country['club'].isin(top_clubs)]
    else:
        df_filtered = df

    payload = {
        "pais": pais,
        "df": df_filtered.to_dict(orient="records")
    }
    url = f"{MICROSERVICE_URL}/obtener_ranking_por_pais"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en obtener_ranking_por_pais: {http_err} - Respuesta: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en obtener_ranking_por_pais: {err}")
    return None