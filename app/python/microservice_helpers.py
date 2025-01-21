import requests
import json

MICROSERVICE_URL = "https://plot-service-163142221066.us-east1.run.app"

def get_plot_top_teams_country(df, country):
    # Armamos un dict con el contenido final
    data_dict = {
        "country": country,
        "df": df.to_dict(orient="records")
    }
    # Convertimos a JSON con default=str para que Timestamps y tipos raros se vuelvan string
    data_json = json.dumps(data_dict, default=str)

    url = f"{MICROSERVICE_URL}/plot_top_teams_country"
    # Enviamos con data=..., y definimos el header Content-Type
    response = requests.post(url, data=data_json, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json().get("image_base64")
    else:
        print("Error en microservicio:", response.text)
        return None


def get_plot_ranking_evolution(df, country):
    data_dict = {
        "country": country,
        "df": df.to_dict(orient="records")
    }
    data_json = json.dumps(data_dict, default=str)

    url = f"{MICROSERVICE_URL}/plot_ranking_evolution"
    response = requests.post(url, data=data_json, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json().get("image_base64")
    else:
        return None


def get_plot_violin_elo(df):
    data_dict = {
        "df": df.to_dict(orient="records")
    }
    data_json = json.dumps(data_dict, default=str)

    url = f"{MICROSERVICE_URL}/plot_violin_elo"
    response = requests.post(url, data=data_json, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json().get("image_base64")
    else:
        return None


def get_plot_heatmap_elo(df):
    data_dict = {
        "df": df.to_dict(orient="records")
    }
    data_json = json.dumps(data_dict, default=str)

    url = f"{MICROSERVICE_URL}/plot_heatmap_elo"
    response = requests.post(url, data=data_json, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json().get("image_base64")
    else:
        return None


def get_plot_team_trend_chart(df, team):
    data_dict = {
        "team": team,
        "df": df.to_dict(orient="records")
    }
    data_json = json.dumps(data_dict, default=str)

    url = f"{MICROSERVICE_URL}/plot_team_trend"
    response = requests.post(url, data=data_json, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json().get("image_base64")
    else:
        return None


def get_ranking_por_pais(df, pais, top_n=5):
    data_dict = {
        "pais": pais,
        "top_n": top_n,
        "df": df.to_dict(orient="records")
    }
    data_json = json.dumps(data_dict, default=str)

    url = f"{MICROSERVICE_URL}/obtener_ranking_por_pais"
    response = requests.post(url, data=data_json, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        # Este endpoint devuelve JSON con rows (no es una imagen)
        return response.json()  # list of dict
    else:
        return None