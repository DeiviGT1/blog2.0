# app/routes.py
from flask import Blueprint, render_template, request, redirect, session
from .python.openai.spotify import app_Authorization as openai_app_Authorization, search_song, user_Authorization as openai_user_Authorization
from .python.openai.openaiapi import generar_respuesta
from .python.spotify.spotify import app_Authorization as playlists_app_Authorization, user_Authorization as playlists_user_Authorization, Profile_Data, Playlist_Data, Song_Data
import pandas as pd
import base64
import json


from dotenv import load_dotenv

# Crear un Blueprint llamado 'main'
main_bp = Blueprint('main', __name__)

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

    for row in avg_per_playlist.iteritems():
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