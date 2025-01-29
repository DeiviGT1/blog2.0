# app/routes/openai_routes.py
from flask import Blueprint, render_template, request, redirect, session
from ..python.openai.spotify import (
    app_Authorization as openai_app_Authorization,
    search_song,
    user_Authorization as openai_user_Authorization
)
from ..python.openai.openaiapi import generar_respuesta

openai_bp = Blueprint('openai', __name__, url_prefix='/openai')

@openai_bp.route('/')
def openai_index():
    return render_template('projects/openai/sonic_surprise.html')

@openai_bp.route("/login", methods=["POST", "GET"])
def login():
    REDIRECT_URI = request.url_root.rstrip('/') + "/callback"
    auth_url = openai_app_Authorization(REDIRECT_URI)
    session["spotify"] = auth_url

    song = request.form.get("song")
    session["song"] = song
    session["artist"] = request.form.get("artist")
    return redirect(auth_url)

@openai_bp.route("/callback")
def callback():
    REDIRECT_URI = request.url_root.rstrip('/') + "/callback"
    header = openai_user_Authorization(REDIRECT_URI)
    session["user"] = header
    return redirect("/song_recommendations")

@openai_bp.route("/song_recommendations", methods=["POST","GET"])
def get_input():
    from flask import jsonify  # Import local para evitar dependencias circulares
    header = session.get("user")
    real_songs = []
    song = session.get("song")
    artist = session.get("artist")
    playlists = generar_respuesta(song, artist)

    lista_nueva = []
    for elemento in playlists:
        elemento_nuevo = elemento.replace("\"", "") \
                                 .replace("\u00f1", "n") \
                                 .replace("\u00e1", "a") \
                                 .replace("\u00e9", "e") \
                                 .replace("\u00ed", "i") \
                                 .replace("\u00f3", "o") \
                                 .replace("\u00fa", "u") \
                                 .replace("¿", "") \
                                 .replace("?", "") \
                                 .replace("¡", "") \
                                 .replace("!", "") \
                                 .replace(".", "") \
                                 .replace(",", "") \
                                 .replace("  ", " ").strip()
        lista_nueva.append(elemento_nuevo)
    
    for song in lista_nueva:
        result = search_song(header=header, song_name=song)
        if result["tracks"]["items"]:
            track = result["tracks"]["items"][0]
            real_songs.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "url": track["external_urls"]["spotify"],
                "image": track["album"]["images"][0]["url"]
            })

    return render_template("projects/openai/recommendations.html", songs=real_songs)