# app/python/spotify/spotify.py

import json
import requests
import base64
import urllib.parse
from flask import request
import os

# Client Keys
CLIENT_ID = "a19b62536391469899844889c65b0d71"
CLIENT_SECRET = os.getenv("SPOTIFY_API_KEY_2")

#Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = f'{SPOTIFY_API_BASE_URL}/{API_VERSION}'

#Server-side Parameters
def get_redirect_uri():
    URL_URI = request.url_root
    REDIRECT = f"{URL_URI}callback"
    return REDIRECT

SCOPE = "user-library-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

#Authorization of application with spotify
def app_Authorization(redirect_uri):
    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": SCOPE,
        "client_id": CLIENT_ID
    }
    url_args = "&".join(["{}={}".format(key, urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"
    return auth_url

#User allows us to acces there spotify
def user_Authorization(redirect_uri):
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": redirect_uri
    }
    client_str = f'{CLIENT_ID}:{CLIENT_SECRET}'
    client_encode = base64.b64encode(client_str.encode("utf-8"))
    client_encode = str(client_encode, "utf-8")
    headers = {"Authorization": f"Basic {client_encode}"}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Use the access token to access Spotify API
    authorization_header = {"Authorization":f"Bearer {access_token}"}
    return authorization_header

#Gathering of profile information
def Profile_Data(header):
    # Get user profile data
    user_profile_api_endpoint = f"{SPOTIFY_API_URL}/me"
    profile_response = requests.get(user_profile_api_endpoint, headers=header)
    profile_data = json.loads(profile_response.text)
    return profile_data

#Gathering of playlist information
def Playlist_Data(header,profile):
    # Get user playlist data
    playlist_api_endpoint = f"{profile['href']}/playlists"
    playlists_response = requests.get(playlist_api_endpoint, headers=header)
    playlist_data = json.loads(playlists_response.text)
    return playlist_data

#Gathering of song information from playlist
def Song_Data(header,playlist):
    # Get user playlist data
    song_api_endpoint = f"{playlist}"
    song_response = requests.get(song_api_endpoint, headers=header)
    song_data = json.loads(song_response.text)
    return song_data

#Gathering of album information
def Album_Data(header,profile,limit,offset):
    # Get user albums data
    artist_api_endpoint = (f"{profile['href']}/albums?limit=" + str(limit) + "&offset=" + str(offset))
    artist_response = requests.get(artist_api_endpoint, headers=header)
    artist_data = json.loads(artist_response.text)
    return artist_data

def logout():
    auth_params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "response_type": "code",
        "redirect_uri": get_redirect_uri(),
        "scope": SCOPE,
        "show_dialog": SHOW_DIALOG_str
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=auth_params)
    token_data = response.json()

    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    revoke_url = "https://accounts.spotify.com/api/token"
    requests.post(revoke_url, headers=headers, data={"token": token})
