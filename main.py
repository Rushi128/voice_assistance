from flask import Flask, request, jsonify, render_template, session
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import smtplib
import requests
import os
# import pyaudio
import random

app = Flask(__name__)
app.secret_key = 'rushi'

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get all available voices
voices = engine.getProperty('voices')

# Set the default voice to female
default_voice_id = voices[1].id

def speak(text, speed=130, voice_id=default_voice_id):
    engine.setProperty('rate', speed)
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-information', methods=['POST'])
def get_information():
    if request.method == 'POST':
        data = request.get_json()
        query = data['query'].lower()

        try:
            if 'hello' in query:
                speak("Hello, Good Day, welcome to MITCORER")
            elif 'open google' in query:
                 if 'search' in query:
                    search_query = query.split('open google and search')[-1].strip()
                    search_google(search_query)
                    speak(f"Searching Google for {search_query}")
                 else:
                    webbrowser.open("https://www.google.com/")
                    speak('Opening Google...')

            elif 'open youtube' in query:
                # webbrowser.open("https://www.youtube.com/")
                # speak('Opening YouTube...')
                if 'search' in query:
                    search_query = query.split('open youtube and search')[-1].strip()
                    search_youtube(search_query)
                    speak(f"Searching on youtube for {search_query}")
                else:
                    webbrowser.open("https://www.youtube.com/")
                    speak('Opening youtube...')

            elif 'open google maps' in query:
                # webbrowser.open("https://www.google.com/maps/")
                # speak('Opening Google Maps...')
                if 'search' in query:
                    search_query = query.split('open google maps and search')[-1].strip()
                    search_google_maps(search_query)
                    speak(f"Searching on google maps for {search_query}")
                else:
                    webbrowser.open("https://www.google.com/maps/")
                    speak('Opening google maps...')

            elif 'play music' in query:
                play_music()
                speak('Playing music...')
            elif 'time' in query:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The current time is {current_time}")
            elif 'date' in query:
                current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                speak(f"Today is {current_date}")
            elif 'female' in query:
                session['voice_id'] = voices[1].id
                speak("Voice changed to female")
            elif 'male' in query:
                session['voice_id'] = voices[0].id
                speak("Voice changed to male")
            elif 'speed' in query:
                speed = int(query.split()[-1])
                speak("Voice speed changed", speed=speed)
            elif 'voice' in query:
                voice_option = query.split()[-1]
                if voice_option.isdigit() and int(voice_option) < len(voices):
                    selected_voice_id = voices[int(voice_option)].id
                    speak("Voice changed", voice_id=selected_voice_id)
                else:
                    speak("Invalid voice option. Please choose a valid voice.")
            elif 'email' in query:
                send_email()
                speak("Sending email.")
            elif 'weather' in query:
                weather_info = get_weather_info()
                speak(f"The weather today is {weather_info}.")
            elif 'joke' in query:
                joke = get_joke()
                speak(joke)
            elif 'reminder' in query:
                set_reminder()
                speak("Setting a reminder.")
            elif 'execute command' in query:
                execute_command(query)
                speak("Executing command.")
            elif 'open google and search' in query:
                search_query = query.split('open google and search')[-1].strip()
                search_google(search_query)
                speak(f"Searching Google for {search_query}")
            elif 'open youtube and search' in query:
                search_query = query.split('open youtube and search')[-1].strip()
                search_youtube(search_query)
                speak(f"Searching YouTube for {search_query}")
            elif 'open google maps and search' in query:
                search_query = query.split('open google maps and search')[-1].strip()
                search_google_maps(search_query)
                speak(f"Searching Google Maps for {search_query}")
            elif 'play music' in query:
                play_music()
                speak('Playing music...')
            else:
                speak("Sorry, I didn't catch that command.")

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand what you said.")
        except sr.RequestError:
            speak("Sorry, there was an error processing your request.")

        return jsonify({'status': 'success'})

def send_email():
    # Configure your email settings
    smtp_server = 'smtp.example.com'
    port = 587
    sender_email = 'your_email@example.com'
    receiver_email = 'recipient_email@example.com'
    password = 'your_email_password'

    subject = 'Test Email'
    body = 'This is a test email.'

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Connect to the SMTP server and send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, f'Subject: {subject}\n\n{body}')

def get_weather_info():
    # Make a request to OpenWeatherMap API (assuming you have an API key)
    api_key = 'your_openweathermap_api_key'
    city = 'New York'  # Example city, you can get this from user input or use a predefined location
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'weather' in data and 'main' in data['weather'][0]:
        weather_main = data['weather'][0]['main']
        return weather_main
    else:
        return 'Weather information not available.'

def get_joke():
    # Example function to fetch a joke from a joke API
    joke_api_url = 'https://api.jokes.one/jod'
    headers = {'Accept': 'application/json'}
    response = requests.get(joke_api_url, headers=headers)
    data = response.json()

    if 'contents' in data and 'jokes' in data['contents'] and data['contents']['jokes']:
        joke_text = data['contents']['jokes'][0]['joke']['text']
        return joke_text
    else:
        return 'No joke available.'

def set_reminder():
    # Example function to set a reminder
    # You can implement this using a database or a reminder service
    pass  # Placeholder for reminder setting logic

def execute_command(command):
    # Example function to execute a command
    # You can implement specific commands here based on user input
    pass  # Placeholder for command execution logic

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)

def search_google_maps(query):
    search_url = f"https://www.google.com/maps/search/{query}"
    webbrowser.open(search_url)

def play_music(song_name=None):
    music_dir = "/home/rishu"  # Update with your music directory path
    songs = os.listdir(music_dir)
    if song_name:
        if f"{song_name}.mp3" in songs:
            os.startfile(os.path.join(music_dir, f"{song_name}.mp3"))
        else:
            speak(f"{song_name} is not available locally. Would you like to play it on YouTube?")
            response = get_user_response()
            while response.lower() not in ['yes', 'no']:
                speak("Please say yes or no.")
                response = get_user_response()
            if response.lower() == 'yes':
                search_youtube(song_name)
                speak(f"Playing {song_name} on YouTube.")
            else:
                speak("Okay, no problem.")
    else:
        if songs:
            index = random.randint(0, len(songs) - 1)
            try:
                os.startfile(os.path.join(music_dir, songs[index]))
            except AttributeError:
                speak(f"Unable to play {songs[index]} locally. Would you like to search it on YouTube?")
                response = get_user_response()
                while response.lower() not in ['yes', 'no']:
                    speak("Please say yes or no.")
                    response = get_user_response()
                if response.lower() == 'yes':
                    search_youtube(songs[index])
                    speak(f"Playing {songs[index]} on YouTube.")
                else:
                    speak("Okay, no problem.")
        else:
            speak("No music files found in the directory.")

def get_user_response():
    # Use speech recognition to get user response
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_response = recognizer.recognize_google(audio).lower()
        return user_response
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        speak(f"Error: {e}")
    return ""  # Return an empty string if there was an error


if __name__ == '__main__':
    app.run(debug=True)
