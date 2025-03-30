import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import genaigoogle
import sys
import os
import shutil
from GoogleNews import GoogleNews

class LoadingScreen:
    def __init__(self, root, loading_image_path="nexa_logo.jpg"):
        self.root = root
        self.root.title("Loading...")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Load and display the loading image
        try:
            self.loading_img = ImageTk.PhotoImage(Image.open(loading_image_path))
            self.img_label = tk.Label(root, image=self.loading_img)
            self.img_label.pack(pady=20)
        except:
            self.img_label = tk.Label(root, text="Loading...", font=("Arial", 16))
            self.img_label.pack(pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start(10)  # Start animation

        # Status label
        self.status = tk.Label(root, text="Initializing Nexa AI...", font=("Arial", 10))
        self.status.pack()

        # Start background task in a thread
        self.running = True
        self.thread = threading.Thread(target=self.run_background_task, daemon=True)
        self.thread.start()

        # Check task status periodically
        self.root.after(100, self.check_task)

    def run_background_task(self):
        """Simulate your actual program initialization"""
        time.sleep(3)  # Replace with your actual program startup
        self.running = False

    def check_task(self):
        if self.running:
            self.root.after(100, self.check_task)
        else:
            self.root.destroy()  # Close loading screen when done

# Usage example
if __name__ == "__main__":
    # Create and show loading screen
    loading_root = tk.Tk()
    loading_app = LoadingScreen(loading_root, "loading.gif")  # Replace with your image
    
    # This blocks until loading screen closes
    loading_root.mainloop()
    
    # Now start your main application
    googlenews = GoogleNews()
    print("Loading complete! Starting main app...")
    main_root = tk.Tk()
    main_root.title("Your Main App")
    image_path = "nexa_logo.jpg"
    img = Image.open(image_path)
    img = img.resize((200, 200))
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(main_root, image=photo)
    label.pack()
    # ... your main application code ...
    # Initialize recognizer
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

        
    def speak(text):
        engine.setProperty('rate', 150)     # setting up new voice rate
        rate = engine.getProperty('rate')   # getting details of current speaking rate                     
        voices = engine.getProperty('voices') #getting details of current voice
        engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female
        engine.say(text)
        engine.runAndWait()
    
    def get_files(directory=os.getcwd()):
        """Returns list of all filenames in directory"""
        print([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)  # Deletes the file
            speak(f"{file_path} deleted successfully!")
        else:
            speak("File does not exist.")
    
    def move_file(source, destination):
        if os.path.exists(source):
            shutil.move(source, destination)  # Moves the file to a new location
            print(f"Moved {source} to {destination}")

    def copy_file(source, destination):
        if os.path.exists(source):
            shutil.copy(source, destination)  #Copies the file to a new location
            print(f"Copied {source} to {destination}")

    def open_file(file_name):
        os.startfile(file_name)
        speak("File Opened")
    
    def mkdir_folder(dir_name):
        os.mkdir(dir_name)
        speak(f"Folder '{dir_name}' created successfully!")
    
    def fetch_news():
        googlenews.get_news('TOP')
        top5 = [article['title'] for article in googlenews.results()[:5]]
        for i in top5:
            speak(i)

    def processCommand(command):
        if "open google" in command.lower():
            webbrowser.open("https://google.co.in")
            speak("Done")
        elif "open spotify" in command.lower():
            webbrowser.open("https://spotify.com")
            speak("Done")
        elif "open youtube" in command.lower():
            webbrowser.open("https://youtube.com")
            speak("Done")
        elif "open facebook" in command.lower():
            webbrowser.open("https://facebook.com")
            speak("Done")
        elif "open linkedin" in command.lower():
            webbrowser.open("https://linkedin.com")
            speak("Done")
        elif command.lower().startswith("play"):
            musiclink=musicLibrary.musics[command.lower()]
            webbrowser.open(musiclink)
            speak("Playing Music")
        elif command.lower()=="shutdown":
            speak("Good Bye")
            print("Good Bye!!")
            sys.exit(0)
        elif command.lower().startswith("open"):
            file_path=command.lower().split()[1]+".py"
            open_file(file_path)

        # elif command.lower().startswith("copy"):
        #     file_path=command.lower().split()[1]+".py"
        #     delete_file(file_path)

        # elif command.lower().startswith("move"):
        #     file_path=command.lower().split()[1]+".py"
        #     delete_file(file_path)

        elif command.lower().startswith("delete"):
            file_path=command.lower().split()[1]+".py"
            delete_file(file_path)

        elif command.lower().startswith("make"):
            file_path=command.lower().split()[1:]
            file_path="_".join(file_path)
            mkdir_folder(file_path)
        
        elif "news" in command.lower():
            fetch_news()
        else:
            # print(f"Fetching results for '{command}'...Please wait...")
            result_text=genaigoogle.clientresponse(command)
            # print(result_text)
            speak(result_text)

    # Use microphone as the source
    if __name__=="__main__":
        speak("Nexa Listening...")
        while True:
            with sr.Microphone() as source:
                print("Recognising...")
                # Keep the icon fixed in position
                # show_icon()
                try:
                    print("Listening...")
                    # recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
                    audio = recognizer.listen(source,timeout=2,phrase_time_limit=1)  # Listen for speech
                    # Convert speech to text using Google's recognizer
                    word = recognizer.recognize_google(audio)
                    if word.lower()=="nexa":
                        speak("Ya")
                        #listen for command
                        with sr.Microphone() as source:
                            print("Activated Nexa!")
                            while True:
                                audio=recognizer.listen(source,timeout=2)
                                command = recognizer.recognize_google(audio)
                                processCommand(command)
                except Exception as e:
                    print("Could not understand the audio")
                    print(f"Error {e}")
                except sr.RequestError:
                    print("Could not request results, check your internet connection")
        #==================================================================#
        main_root.mainloop()