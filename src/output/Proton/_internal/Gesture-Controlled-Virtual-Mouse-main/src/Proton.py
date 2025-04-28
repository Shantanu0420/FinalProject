import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
import app
from threading import Thread
import pywhatkit as kit  # Import pywhatkit for playing music from YouTube

# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status

# ------------------Functions----------------------

def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")
        
    reply("I am Tiger, how may I help you?")  # Changed to Tiger

# Set Microphone parameters
with sr.Microphone() as source:
    r.energy_threshold = 500
    r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry, my service is down. Please check your Internet connection.')
        except sr.UnknownValueError:
            print('Can\'t recognize the speech.')
            pass
        return voice_data.lower()

# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(f"Received Command: {voice_data}")
    voice_data = voice_data.replace('tiger', '')  # Removed "tiger" if it exists
    app.eel.addUserMsg(voice_data)

    if is_awake == False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Tiger!')  # Changed to Tiger

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        search_term = voice_data.split('search')[1].strip()
        reply(f'Searching for {search_term}')
        url = 'https://google.com/search?q=' + search_term
        try:
            webbrowser.get().open(url)
            reply('This is what I found, Sir.')
        except:
            reply('Please check your Internet connection.')

    elif 'location' in voice_data:
        reply('Which place are you looking for?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found, Sir.')
        except:
            reply('Please check your Internet connection.')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Goodbye Sir! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        sys.exit()

    # DYNAMIC CONTROLS
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active.')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target=gc.start)
            t.start()
            reply('Launched successfully.')

    elif ('stop gesture recognition' in voice_data) or ('stop gesture recognition' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped.')
        else:
            reply('Gesture recognition is already inactive.')

    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied.')

    elif 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted.')

    # Play Music Command (YouTube)
    elif 'play' in voice_data and 'music' in voice_data:
        song_name = voice_data.split('play music')[-1].strip()  # Get the song name after the command "play music"
        play_music_on_youtube(song_name)  # Play the music using the defined function

    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter += 1
            print(f"{counter}: {f}")
            filestr += f"{counter}: {f}<br>"
        file_exp_status = True
        reply('These are the files in your root directory:')
        app.ChatBot.addAppMsg(filestr)

    elif file_exp_status:
        counter = 0
        if 'open' in voice_data:
            try:
                index = int(voice_data.split(' ')[-1]) - 1
                if isfile(join(path, files[index])):
                    os.startfile(path + files[index])
                    file_exp_status = False
                else:
                    path = path + files[index] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter += 1
                        filestr += f"{counter}: {f}<br>"
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)

            except Exception as e:
                reply(f"Error: {str(e)}")

        elif 'back' in voice_data:
            if path == 'C://':
                reply('Sorry, this is the root directory.')
            else:
                path = '//'.join(path.split('//')[:-2]) + '//'
                files = listdir(path)
                filestr = ""
                for f in files:
                    counter += 1
                    filestr += f"{counter}: {f}<br>"
                reply('Ok')
                app.ChatBot.addAppMsg(filestr)
    else: 
        reply('I am not functioned to do this!')

# Play Music on YouTube
def play_music_on_youtube(song_name):
    try:
        kit.playonyt(song_name)  # This will search and play the song on YouTube
        reply(f"Playing {song_name} on YouTube for you!")
    except Exception as e:
        reply(f"There was an issue playing the song. Error: {str(e)}")

# ------------------Driver Code--------------------

def main():
    print("Starting the assistant...")

    # Start the chatbot thread
    t1 = Thread(target=app.ChatBot.start)
    t1.start()

    # Lock main thread until Chatbot has started
    while not app.ChatBot.started:
        time.sleep(0.5)

    # Greet the user
    wish()

    while True:
        voice_data = record_audio()

        if 'tiger' in voice_data:  # Changed to Tiger
            try:
                respond(voice_data)
            except SystemExit:
                reply("Exit successful.")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

# Run the main function if the script is run directly
if __name__ == "__main__":
    main()
