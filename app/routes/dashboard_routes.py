# app/routes/dashboard_routes.py
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import base64
import json
from ..python.dashboard.data import load_data
from ..python.microservice_helpers import (
    get_plot_top_teams_country,
    get_plot_ranking_evolution,
    get_plot_violin_elo,
    get_plot_heatmap_elo,
    get_plot_team_trend_chart,
    get_ranking_por_pais
)

from ..python.dashboard.ai import generate_conclusions
import logging

dashboard_bp = Blueprint('dashboard', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar datos una vez al iniciar el módulo
df = load_data("app/static/csv/EloRatings.csv")

@dashboard_bp.route("/dashboard_index", methods=["GET"])
def dashboard_index():
    """
    Renderiza la página principal con la lista de países y clubes.
    Las gráficas se actualizarán vía AJAX.
    """
    countries_list = sorted(df['country'].unique())
    clubs_list = sorted(df['club'].unique())

    return render_template("projects/dashboard/elo_dynamic_charts.html",
                           countries=countries_list,
                           clubs=clubs_list)
    
@dashboard_bp.route("/update_charts", methods=["POST"])
def update_charts():
    data = request.get_json()
    country_bar = data.get("country_bar")
    country_rank = data.get("country_rank")
    show_violin = data.get("show_violin", False)
    show_heatmap = data.get("show_heatmap", False)
    teams = data.get("teams", [])

    # Crear una copia del DataFrame para evitar modificar el original
    df_copy = df.copy()

    # Identificar y convertir todas las columnas de tipo datetime a cadenas
    datetime_columns = df_copy.select_dtypes(include=['datetime', 'datetime64[ns]']).columns
    for col in datetime_columns:
        df_copy[col] = df_copy[col].dt.strftime('%Y-%m-%d')  # Puedes ajustar el formato según tus necesidades

    # Generar los gráficos utilizando tus funciones de plotting
    trend_chart = get_plot_team_trend_chart(df_copy, teams) if teams else None
    bar_chart = get_plot_top_teams_country(df_copy, country_bar) if country_bar else None
    rank_chart = get_plot_ranking_evolution(df_copy, country_rank) if country_rank else None
    violin_chart = get_plot_violin_elo(df_copy) if show_violin else None
    heatmap_chart = get_plot_heatmap_elo(df_copy) if show_heatmap else None


    return jsonify({
        "trend_chart": trend_chart,
        "bar_chart": bar_chart,
        "rank_chart": rank_chart,
        "violin_chart": violin_chart,
        "heatmap_chart": heatmap_chart
    })

@dashboard_bp.route("/generate_conclusions_ajax", methods=["POST"])
def generate_conclusions_ajax():
    """
    Genera conclusiones con IA basadas en el tipo de gráfico y los filtros aplicados.
    """
    data = request.get_json()

    chart_type = data.get("chart_type")
    country_bar = data.get("country_bar")
    country_rank = data.get("country_rank")
    show_violin = data.get("show_violin", False)
    show_heatmap = data.get("show_heatmap", False)
    team_trend = data.get("team_trend")

    chart_df = None
    extra_info = {}

    # Dependiendo del tipo de gráfico, filtramos el DataFrame
    if chart_type == "bar_chart" and country_bar:
        df_country = df[df['country'] == country_bar]
        top5 = (df_country.groupby('club')['elo'].mean()
                .reset_index()
                .sort_values('elo', ascending=False)
                .head(5))
        chart_df = top5
        extra_info['country'] = country_bar

    elif chart_type == "ranking_chart" and country_rank:
        ranking_df_proc = get_ranking_por_pais(df, country_rank, top_n=3)
        chart_df = ranking_df_proc
        extra_info['country'] = country_rank

    elif chart_type == "violin_plot":
        # Suponemos que violin usa todo df
        chart_df = df

    elif chart_type == "heatmap":
        # Heatmap usa pivot table
        pivot_elo = df.pivot_table(index='club', columns='year', values='elo', aggfunc='mean')
        heatmap_df = pivot_elo.reset_index()
        chart_df = heatmap_df

    elif chart_type == "team_trend_chart" and team_trend:
        # team_trend ahora es una lista de equipos separados por comas
        teams = [team.strip() for team in team_trend.split(",")]
        df_team = df[df['club'].isin(teams)]
        chart_df = df_team
        extra_info['teams'] = teams

    if chart_df is not None and not chart_df.empty:
        text = generate_conclusions(chart_type, chart_df, extra_info)
    else:
        text = "No se encontraron datos para este gráfico."

    return jsonify({"conclusions": text})