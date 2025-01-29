# app/python/microservice_helpers.py

import requests
import json
import logging
import pandas as pd

# URL base de tu microservicio de graficación en Cloud Run
MICROSERVICE_URL = "https://microservice-plot-163142221066.us-central1.run.app"

# Configuración del logger para registrar errores y eventos
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_datetime_columns_to_str(df):
    """
    Convierte todas las columnas de tipo datetime en el DataFrame a strings en formato 'YYYY-MM-DD'.

    Parámetros:
        df (pd.DataFrame): DataFrame original.

    Retorna:
        pd.DataFrame: DataFrame con columnas datetime convertidas a strings.
    """
    df = df.copy()
    datetime_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime']).columns
    for col in datetime_columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d')
    return df

def get_plot_team_trend_chart(df, teams):
    """
    Solicita al microservicio generar un gráfico de tendencia ELO para múltiples equipos.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos necesarios.
        teams (list): Lista de nombres de equipos a graficar.

    Retorna:
        str: Imagen en formato base64 si la solicitud es exitosa, de lo contrario, None.
    """
    # Convertir columnas datetime a string
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
        logger.error(f"HTTP error en plot_team_trend: {http_err} - Respuesta del servidor: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en plot_team_trend: {err}")
    return None


def get_plot_top_teams_country(df, country):
    """
    Solicita al microservicio generar un gráfico de los top equipos por país.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos necesarios.
        country (str): Nombre del país para filtrar los equipos.

    Retorna:
        str: Imagen en formato base64 si la solicitud es exitosa, de lo contrario, None.
    """
    # Convertir columnas datetime a string
    df = convert_datetime_columns_to_str(df)
    
    payload = {
        "country": country,
        "df": df.to_dict(orient="records")
    }

    url = f"{MICROSERVICE_URL}/plot_top_teams_country"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        image = response.json().get("image_base64")
        return image
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en plot_top_teams_country: {http_err} - Respuesta del servidor: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en plot_top_teams_country: {err}")
    return None


def get_plot_ranking_evolution(df, country):
    """
    Solicita al microservicio generar un gráfico de la evolución del ranking.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos necesarios.
        country (str): Nombre del país para filtrar los equipos.

    Retorna:
        str: Imagen en formato base64 si la solicitud es exitosa, de lo contrario, None.
    """
    # Convertir columnas datetime a string
    df = convert_datetime_columns_to_str(df)
    
    payload = {
        "country": country,
        "df": df.to_dict(orient="records")
    }

    url = f"{MICROSERVICE_URL}/plot_ranking_evolution"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json().get("image_base64")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en plot_ranking_evolution: {http_err} - Respuesta del servidor: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en plot_ranking_evolution: {err}")
    return None


def get_plot_violin_elo(df):
    """
    Solicita al microservicio generar un Violin Plot de ELO por país.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos necesarios.

    Retorna:
        str: Imagen en formato base64 si la solicitud es exitosa, de lo contrario, None.
    """
    # Convertir columnas datetime a string
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
        logger.error(f"HTTP error en plot_violin_elo: {http_err} - Respuesta del servidor: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en plot_violin_elo: {err}")
    return None


def get_plot_heatmap_elo(df):
    """
    Solicita al microservicio generar un Heatmap de ELO por club y año.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos necesarios.

    Retorna:
        str: Imagen en formato base64 si la solicitud es exitosa, de lo contrario, None.
    """
    # Convertir columnas datetime a string
    df = convert_datetime_columns_to_str(df)
    
    payload = {
        "df": df.to_dict(orient="records")
    }

    url = f"{MICROSERVICE_URL}/plot_heatmap_elo"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json().get("image_base64")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en plot_heatmap_elo: {http_err} - Respuesta del servidor: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en plot_heatmap_elo: {err}")
    return None


def get_ranking_por_pais(df, pais, top_n=5):
    """
    Solicita al microservicio obtener el ranking de equipos por país.

    Parámetros:
        df (pd.DataFrame): DataFrame con los datos necesarios.
        pais (str): Nombre del país para filtrar los equipos.
        top_n (int): Número de equipos a incluir en el ranking.

    Retorna:
        list of dict: Lista de diccionarios con el ranking si la solicitud es exitosa, de lo contrario, None.
    """
    # Convertir columnas datetime a string
    df = convert_datetime_columns_to_str(df)
    
    payload = {
        "pais": pais,
        "top_n": top_n,
        "df": df.to_dict(orient="records")
    }

    url = f"{MICROSERVICE_URL}/obtener_ranking_por_pais"
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()  # Devuelve una lista de diccionarios
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error en obtener_ranking_por_pais: {http_err} - Respuesta del servidor: {response.text}")
    except Exception as err:
        logger.error(f"Error inesperado en obtener_ranking_por_pais: {err}")
    return None