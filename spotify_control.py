import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env.local")

# Spotify API setup
scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope=scope
))

def play_song(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])

    if not tracks:
        print("❌ No song found.")
        return "Sir, I couldn't find the song you requested."

    uri = tracks[0]['uri']
    sp.start_playback(uris=[uri])
    print(f"▶️ Playing: {tracks[0]['name']} by {tracks[0]['artists'][0]['name']}")
    return f"Now playing {tracks[0]['name']} by {tracks[0]['artists'][0]['name']}."

def pause_playback():
    sp.pause_playback()
    return "Playback paused, sir."

def resume_playback():
    sp.start_playback()
    return "Resuming playback, sir."

def next_track():
    sp.next_track()
    return "Skipping to the next track, sir."

def previous_track():
    sp.previous_track()
    return "Going back to the previous track, sir."
