# app/routes.py
from flask import Blueprint, render_template, request, redirect, session, jsonify
from .python.openai.spotify import app_Authorization as openai_app_Authorization, search_song, user_Authorization as openai_user_Authorization
from .python.openai.openaiapi import generar_respuesta
from .python.spotify.spotify import app_Authorization as playlists_app_Authorization, user_Authorization as playlists_user_Authorization, Profile_Data, Playlist_Data, Song_Data
import pandas as pd
import base64
import json
from .python.dashboard.data import load_data
from .python.dashboard.plotting import (
    plot_top_teams_country,
    plot_ranking_evolution,
    plot_violin_elo,
    plot_heatmap_elo,
    obtener_ranking_por_pais,
    plot_team_trend_chart
)
from .python.dashboard.ai import generate_conclusions  # Lógica para IA con requests


from dotenv import load_dotenv

# Crear un Blueprint llamado 'main'
main_bp = Blueprint('main', __name__)
df = load_data("app/static/csv/Eloratings.csv")

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/openai')
def openai():
    return render_template('projects/openai/sonic_surprise.html')

@main_bp.route("/login", methods=["POST", "GET"])
def login():
    REDIRECT_URI = request.url_root.rstrip('/') + "/callback"
    auth_url = openai_app_Authorization(REDIRECT_URI)
    session["spotify"] = auth_url

    song = request.form["song"]
    session["song"] = song
    session["artist"] = request.form["artist"]
    return redirect(auth_url)

@main_bp.route("/callback")
def callback():
    REDIRECT_URI = request.url_root.rstrip('/') + "/callback"
    header = openai_user_Authorization(REDIRECT_URI)
    session["user"] = header
    return redirect("/song_recommendations")

@main_bp.route("/song_recommendations", methods=["POST","GET"])
def get_input():
    header = session.get("user")
    real_songs = []
    song = session.get("song")
    artist = session.get("artist")
    playlists = generar_respuesta(song, artist)

    lista_nueva = []
    for elemento in playlists:
        elemento_nuevo = elemento.replace("\"", "").replace("\u00f1", "n").replace("\u00e1", "a").replace("\u00e9", "e").replace("\u00ed", "i").replace("\u00f3", "o").replace("\u00fa", "u").replace("¿", "").replace("?", "").replace("¡", "").replace("!", "").replace(".", "").replace(",", "").replace("  ", " ").strip()
        lista_nueva.append(elemento_nuevo)
    
    for song in lista_nueva:
        result = search_song(header = header, song_name = song)
        if len(result["tracks"]["items"]) > 0:
            track_id = result["tracks"]["items"][0]["id"]
            track_image = result["tracks"]["items"][0]["album"]["images"][0]["url"]
            track_name = result["tracks"]["items"][0]["name"]
            track_artists = result["tracks"]["items"][0]["artists"][0]["name"]
            track_url = result["tracks"]["items"][0]["external_urls"]["spotify"]
            
            real_songs.append({"name": track_name, "artist":track_artists , "url": track_url, "image": track_image})

    return render_template("projects/openai/recommendations.html", songs = real_songs)

@main_bp.route("/playlists")
def playlists_index():
    return render_template("projects/spotify/index.html")

@main_bp.route("/playlists/login")
def playlists_login():
    REDIRECT_URI = request.url_root.rstrip('/') + "/playlists/callback"
    auth_url = playlists_app_Authorization(REDIRECT_URI)
    session["playlists_auth_url"] = auth_url
    return redirect(auth_url)

@main_bp.route("/playlists/callback")
def playlists_callback():
    REDIRECT_URI = request.url_root.rstrip('/') + "/playlists/callback"
    authorization_header = playlists_user_Authorization(REDIRECT_URI)
    session["playlists_authorization_header"] = authorization_header

    # Recolección de datos del perfil
    profile_data = Profile_Data(authorization_header)
    user_id = profile_data["id"]
    user_name = profile_data["display_name"]

    # Recolección de datos de playlists y canciones
    playlist_data = Playlist_Data(authorization_header, profile_data)
    avg_dicts = []
    final_result = []

    for items in playlist_data.get("items", []):
        playlist_name = items["name"]
        playlist_url = items["external_urls"]["spotify"]
        url = items["tracks"]["href"]
        song_data = Song_Data(authorization_header, url)
        for song in song_data.get("items", []):
            avg_dicts.append({
                "id": song["track"]["id"],
                "name": song["track"]["name"],
                "artist": song["track"]["artists"][0]["name"],
                "playlist_name": playlist_name,
                "playlist_url": playlist_url,
                "added_at": song["added_at"],
                "user_id": user_id,
                "user_name": user_name,
                "duration_ms": song["track"]["duration_ms"],
                "popularity": song["track"]["popularity"],
                "explicit": song["track"]["explicit"],
                "amount_available_markets": len(song["track"]["available_markets"]),
            })

    if not avg_dicts:
        print("No se encontraron canciones en las playlists.")
        # Puedes redirigir o mostrar un mensaje de error apropiado
        return render_template("projects/spotify/playlist.html", avg_per_playlist_base64='')

    df = pd.DataFrame(avg_dicts)
    avg_per_playlist = df.groupby(["playlist_name", "playlist_url"]).mean(numeric_only=True)["popularity"]

    for row in avg_per_playlist.items():
        final_result.append({
            "playlist_name": row[0][0],
            "playlist_url": row[0][1],
            "avg_popularity": "{:.2f}".format(row[1])
        })

    # Convierte final_result a JSON y luego a Base64
    data_json = json.dumps(final_result)
    data_base64 = base64.b64encode(data_json.encode('utf-8')).decode('utf-8')

    print('final_result:', final_result)
    print('avg_per_playlist_base64:', data_base64)

    return render_template("projects/spotify/playlist.html", avg_per_playlist_base64=data_base64)

@main_bp.route("/playlists/logout")
def playlists_logout():
    session.pop("playlists_authorization_header", None)
    session.clear()
    return redirect("/playlists")

@main_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    # Listas para los selects
    countries_list = sorted(df['country'].unique())
    clubs_list = sorted(df['club'].unique())

    # Variables de control
    selected_country_bar = None
    selected_country_rank = None
    selected_team_trend = None
    show_violin = False
    show_heatmap = False

    # Imágenes en base64 para los gráficos (inicialmente None)
    bar_image_base64 = None
    rank_image_base64 = None
    violin_image_base64 = None
    heatmap_image_base64 = None
    team_trend_image_base64 = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "generate_charts":
            # Obtener datos del formulario
            selected_country_bar = request.form.get("country_bar")
            selected_country_rank = request.form.get("country_rank")
            selected_team_trend = request.form.get("team_trend_club")
            show_violin = (request.form.get("show_violin") == "on")
            show_heatmap = (request.form.get("show_heatmap") == "on")

            # Generación de gráficos
            if selected_country_bar:
                bar_image_base64 = plot_top_teams_country(df, selected_country_bar)
            if selected_country_rank:
                rank_image_base64 = plot_ranking_evolution(df, selected_country_rank)
            if show_violin:
                violin_image_base64 = plot_violin_elo(df)
            if show_heatmap:
                heatmap_image_base64 = plot_heatmap_elo(df)
            if selected_team_trend:
                
                team_trend_image_base64 = plot_team_trend_chart(df, selected_team_trend)

    return render_template(
        "projects/dashboard/dashboard.html",
        countries=countries_list,
        clubs=clubs_list,
        selected_country_bar=selected_country_bar,
        selected_country_rank=selected_country_rank,
        selected_team_trend=selected_team_trend,
        show_violin=show_violin,
        show_heatmap=show_heatmap,
        bar_image_base64=bar_image_base64,
        rank_image_base64=rank_image_base64,
        violin_image_base64=violin_image_base64,
        heatmap_image_base64=heatmap_image_base64,
        team_trend_image_base64=team_trend_image_base64
    )

@main_bp.route("/generate_conclusions_ajax", methods=["POST"])
def generate_conclusions_ajax():
    data = request.get_json()

    chart_type = data.get("chart_type")
    country_bar = data.get("country_bar")
    country_rank = data.get("country_rank")
    team_trend = data.get("team_trend")
    show_violin = data.get("show_violin", False)
    show_heatmap = data.get("show_heatmap", False)

    chart_df = None
    extra_info = {}  # Se añade el idioma

    if chart_type == "bar_chart" and country_bar:
        df_country = df[df['country'] == country_bar]
        top5 = (df_country.groupby('club')['elo'].mean()
                .reset_index()
                .sort_values('elo', ascending=False)
                .head(5))
        chart_df = top5
        extra_info['country'] = country_bar

    elif chart_type == "ranking_chart" and country_rank:
        ranking_df_proc = obtener_ranking_por_pais(df, country_rank, top_n=5)
        chart_df = ranking_df_proc
        extra_info['country'] = country_rank

    elif chart_type == "violin_plot":
        chart_df = df

    elif chart_type == "heatmap":
        pivot_elo = df.pivot_table(index='club', columns='year', values='elo', aggfunc='mean')
        heatmap_df = pivot_elo.reset_index()
        chart_df = heatmap_df

    elif chart_type == "team_trend_chart" and team_trend:
        df_team = df[df['club'] == team_trend]
        chart_df = df_team
        extra_info['team'] = team_trend

    if chart_df is not None and not chart_df.empty:
        text = generate_conclusions(chart_type, chart_df, extra_info)
    else:
        text = "No se encontraron datos para este gráfico."

    return jsonify({"conclusions": text})