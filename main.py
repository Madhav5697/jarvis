import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import urllib.parse
from ai_api import call_api
from spotify_control import play_song, pause_playback, resume_playback, next_track, previous_track
from weathe_api import get_weather
from news_api import get_news

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"JARVIS : {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening (English)...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language='en-IN')
        print(f"🗣️ You said: {command}")
        return command.lower()
    except:
        print("❌ Didn't catch that.")
        return ""

def open_brave():
    try:
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
        webbrowser.get('brave').open("https://www.google.com")
    except Exception as e:
        print(f"⚠️ Could not open Brave: {e}")
        speak("Sorry sir, I couldn't open Brave browser.")

def open_youtube(query=None):
    try:
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))

        if query:
            search = urllib.parse.quote(query)
            url = f"https://www.youtube.com/results?search_query={search}"
            speak(f"Playing {query} on YouTube")
        else:
            url = "https://www.youtube.com/"
            speak("Opening YouTube in Brave")

        webbrowser.get('brave').open(url)

    except Exception as e:
        print(f"⚠️ Could not open YouTube: {e}")
        speak("Sorry sir, couldn't open YouTube.")

def main_jarvis():
    speak("How may I assist you?")
    while True:
        command = listen()
        if not command:
            continue

        # 🎵 Spotify voice control
        if "play song" in command or "on spotify" in command:
            song = command.replace("play song", "").replace("on spotify", "").strip()
            response = play_song(song)
            speak(response)

        elif "pause music" in command or "pause song" in command:
            speak(pause_playback())

        elif "resume music" in command or "continue song" in command:
            speak(resume_playback())

        elif "next song" in command or "skip song" in command:
            speak(next_track())

        elif "previous song" in command:
            speak(previous_track())

        # 🌐 Brave or YouTube
        elif "open brave" in command or "launch browser" in command or "start brave" in command:
            speak("Opening Brave browser.")
            open_brave()

        elif "youtube" in command and "play" not in command:
            open_youtube()

        elif "play" in command and "on youtube" in command:
            query = command.replace("play", "").replace("on youtube", "").strip()
            open_youtube(query)

        # 🌦️ Weather
        elif "weather" in command:
            city = "Hospet"
            words = command.split()
            for i, word in enumerate(words):
                if word == "in" and i + 1 < len(words):
                    city = words[i + 1]
                    break
            speak(f"Fetching weather in {city}, sir.")
            weather = get_weather(city)
            speak(weather)

        # 📰 News
        elif "news" in command or "headlines" in command:
            category = "general"
            country = "in"  # Default: India

            # Category detection
            if "tech" in command:
                category = "technology"
            elif "sports" in command:
                category = "sports"
            elif "business" in command:
                category = "business"
            elif "entertainment" in command:
                category = "entertainment"
            elif "health" in command:
                category = "health"
            elif "science" in command:
                category = "science"

            # Country detection
            if "international" in command or "global" in command or "world" in command:
                country = "us"
            elif "national" in command or "india" in command:
                country = "in"

            speak(f"Fetching {category} news from {('international' if country == 'us' else 'India')} for you, sir.")
            news = get_news(category, country)
            speak(news)

        # 🔚 Exit trigger
        elif any(x in command for x in ["exit", "stop", "bye", "have to go"]):
            speak("Going back to standby.")
            break
        else:
            reply=call_api(command)
            speak(reply)

def passive_listener():
    speak("System in standby mode.")
    while True:
        command = listen()
        if "wake up" or "hello" or "hi" or "jarvis" in command:
            speak("Welcome back sir. Initializing systems.")
            main_jarvis()
            speak("Returning to standby mode.")
        elif "dismiss" in command:
            speak("Shutting down. Goodbye sir.")
            break

if __name__ == "__main__":
    passive_listener()
