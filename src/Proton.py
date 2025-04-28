import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
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
import pywhatkit as kit

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
    reply("I am Tiger, how may I help you?")

with sr.Microphone() as source:
    r.energy_threshold = 500
    r.dynamic_energy_threshold = False

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
        return voice_data.lower()

def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(f"Received Command: {voice_data}")
    voice_data = voice_data.replace('tiger', '').strip().lower()
    app.eel.addUserMsg(voice_data)

    if not is_awake:
        if 'wake up' in voice_data:
            is_awake = True
            wish()
        return

    if 'hello' in voice_data:
        wish()
    elif 'what is your name' in voice_data:
        reply('My name is Tiger!')
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
    elif 'bye' in voice_data or 'by' in voice_data:
        reply("Goodbye Sir! Have a nice day.")
        is_awake = False
    elif 'exit' in voice_data or 'terminate' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        sys.exit()
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active.')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target=gc.start)
            t.start()
            reply('Launched successfully.')
    elif 'stop gesture recognition' in voice_data:
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
    elif 'play' in voice_data and 'music' in voice_data:
        song_name = voice_data.split('play music')[-1].strip()
        play_music_on_youtube(song_name)
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

def play_music_on_youtube(song_name):
    try:
        kit.playonyt(song_name)
        reply(f"Playing {song_name} on YouTube for you!")
    except Exception as e:
        reply(f"There was an issue playing the song. Error: {str(e)}")

# --------------User Manual with Image + Timer---------------
def show_user_manual():
    manual_window = tk.Tk()
    manual_window.title("Tiger Assistant - User Manual")
    manual_window.geometry("780x580")
    manual_window.configure(bg="#f0f0f0")

    # Canvas & Scrollbar setup
    canvas = tk.Canvas(manual_window, bg="#f0f0f0")
    scrollbar = tk.Scrollbar(manual_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set, bg="#f0f0f0")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Heading
    heading_label = tk.Label(scrollable_frame, text="👋 Gesture Control Instructions", font=("Helvetica", 22, "bold"), bg="#f0f0f0", fg="#2c3e50")
    heading_label.pack(pady=(15, 10))

    # Image (if available)
    try:
        image = Image.open("Tushar.jpeg")
        image = image.resize((720, 300))
        img = ImageTk.PhotoImage(image)
        panel = tk.Label(scrollable_frame, image=img, bg="#f0f0f0")
        panel.image = img
        panel.pack(pady=10)
    except:
        fallback_label = tk.Label(scrollable_frame, text="(Image failed to load)", font=("Arial", 10), fg="red", bg="#f0f0f0")
        fallback_label.pack(pady=10)


    # Heading
    heading_label = tk.Label(scrollable_frame, text="👋 Voice Assistance  Control Instructions", font=("Helvetica", 22, "bold"), bg="#f0f0f0", fg="#2c3e50")
    heading_label.pack(pady=(15, 10))

    # Helper to add command sections
    def add_section(title, commands, bg_color="#ffffff", icon="📌"):
        section = tk.Frame(scrollable_frame, bg=bg_color, padx=10, pady=10, highlightbackground="#cccccc", highlightthickness=1)
        title_label = tk.Label(section, text=f"{icon} {title}", font=("Helvetica", 16, "bold"), bg=bg_color, fg="#333")
        title_label.pack(anchor="w")

        for cmd in commands:
            cmd_label = tk.Label(section, text="• " + cmd, font=("Arial", 12), anchor="w", justify="left", bg=bg_color)
            cmd_label.pack(anchor="w", padx=10, pady=2)

        section.pack(fill="x", padx=20, pady=8)

    # Sections
    add_section("Voice Activation", [
        'Say "Tiger" to activate voice input',
        'Then speak your command'
    ], bg_color="#eaf2f8", icon="🎤")

    add_section("General Commands", [
        'What is the time?',
        'What is the date today?',
        'Open file explorer',
        'Search for [your query]',
        'Play music [song name]',
        'Tell me a joke'
    ], bg_color="#fef9e7", icon="🔍")

    add_section("File & Application Control", [
        'Open Notepad',
        'Open Calculator',
        'Close Notepad',
        'Close Calculator'
    ], bg_color="#fcf3cf", icon="🗂")

    add_section("Location & Internet Search", [
        'Search weather in [city]',
        'Where is Eiffel Tower?'
    ], bg_color="#f5eef8", icon="🌐")

    add_section("Clipboard Commands", [
        'Copy',
        'Paste',
        'Cut',
        'Select all'
    ], bg_color="#e8f8f5", icon="📋")

    add_section("Gesture Mouse Control", [
        'Launch gesture recognition',
        'Stop gesture recognition'
    ], bg_color="#f9ebea", icon="🖱")

    add_section("Exit Commands", [
        'Say "Bye" – stops voice listening',
        'Say "Exit" – closes the assistant'
    ], bg_color="#f5f5f5", icon="🛑")

    # Tip section
    tip_label = tk.Label(
        scrollable_frame,
        text="💡 Tip: Keep your microphone on and speak clearly for best results.",
        font=("Arial", 12, "italic"),
        bg="#f0f0f0",
        fg="#555"
    )
    tip_label.pack(pady=(10, 20))

    def close_manual():
        manual_window.destroy()
        main()  # Make sure main() exists in your code

    manual_window.after(60000, close_manual)  # Auto-close after 60 seconds
    manual_window.mainloop()

# ------------------Driver Code--------------------
def main():
    print("Starting the assistant...")
    t1 = Thread(target=app.ChatBot.start)
    t1.start()

    while not app.ChatBot.started:
        time.sleep(0.5)

    wish()

    while True:
        voice_data = record_audio()
        if 'tiger' in voice_data:
            try:
                respond(voice_data)
            except SystemExit:
                reply("Exit successful.")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    show_user_manual()
