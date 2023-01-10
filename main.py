from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')

#mikon toimiva
song_names_long = soup.find_all("h3", id="title-of-a-story", class_="a-no-trucate")  # <class bs4.Beautifulsoup>
song_names = [song.getText().strip() for song in song_names_long]

#kurssin ei-toimiva
# song_names_spans = soup.find_all("h3", id="title-of-a-story")
# print(f"song_names_spans = {song_names_spans}")
# song_names = [song.getText() for song in song_names_spans]
# print(f"song_names = {song_names}")


#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="",   # hae sieltä d:ltä
        client_secret="",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(f"user_id {user_id}")

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    print("in for")
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(f"result = {result}")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(f"song uris: {song_uris}")

print(f"date = {date}")
#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(f"playlist = {playlist}")

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)