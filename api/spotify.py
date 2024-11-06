from flask import request
import os
import json
import requests
import base64
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
# Client Keys

CLIENT_ID = "e68285acd05e49bb9134e5bcc2622778"
CLIENT_SECRET = os.getenv("SPOTIFY_API_KEY")

#Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = f'{SPOTIFY_API_BASE_URL}/{API_VERSION}'

SCOPE = "user-library-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

#Server-side Parameters
def get_redirect_uri():
    URL_URI = request.url_root
    REDIRECT = f"{URL_URI}callback"
    return REDIRECT

#Authorization of application with spotify
def app_Authorization():
    REDIRECT_URI = get_redirect_uri()
    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        # "state": STATE,
        # "show_dialog": SHOW_DIALOG_str,
        "client_id": CLIENT_ID
    }
    url_args = "&".join(["{}={}".format(key, urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"

    return auth_url

#User allows us to acces there spotify
def user_Authorization():
    REDIRECT_URI = get_redirect_uri()
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
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

def Profile_Data(header):
    # Get user profile data
    user_profile_api_endpoint = f"{SPOTIFY_API_URL}/me"
    profile_response = requests.get(user_profile_api_endpoint, headers=header)
    profile_data = json.loads(profile_response.text)
    return profile_data

# Get user albums data
def get_user_liked_songs(header):
    # Get profile data
    user_profile_api_endpoint = f"{SPOTIFY_API_URL}/me/tracks"
    profile_response = requests.get(user_profile_api_endpoint, headers=header, params={"limit": 50})
    profile_data = json.loads(profile_response.text)
    return profile_data

def search_song(header, song_name):
    # Get profile data
    user_profile_api_endpoint = f"{SPOTIFY_API_URL}/search"
    profile_response = requests.get(user_profile_api_endpoint, headers=header, params={"q": song_name, "type": "track", "limit": 1})
    profile_data = json.loads(profile_response.text)
    return profile_data