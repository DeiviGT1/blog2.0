# app/routes/playlists_routes.py
from flask import Blueprint, render_template, request, redirect, session
from ..python.spotify.spotify import (
    app_Authorization as playlists_app_Authorization,
    user_Authorization as playlists_user_Authorization,
    Profile_Data,
    Playlist_Data,
    Song_Data
)
import pandas as pd
import base64
import json

playlists_bp = Blueprint('playlists', __name__, url_prefix='/playlists')

@playlists_bp.route('/')
def playlists_index():
    return render_template("projects/spotify/index.html")

@playlists_bp.route("/login")
def playlists_login():
    REDIRECT_URI = request.url_root.rstrip('/') + "/playlists/callback"
    auth_url = playlists_app_Authorization(REDIRECT_URI)
    session["playlists_auth_url"] = auth_url
    return redirect(auth_url)

@playlists_bp.route("/callback")
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

@playlists_bp.route("/logout")
def playlists_logout():
    session.pop("playlists_authorization_header", None)
    session.clear()
    return redirect("/playlists")