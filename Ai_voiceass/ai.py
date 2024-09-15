import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import psutil
import pyjokes
import sys
import os

engine = pyttsx3.init()
recognizer = sr.Recognizer()

newsapi = "5ac420cd777d4471a1df91fec1"
weatherapi = "ef882dd4f56af44fa964"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather():
    city = "Nashik"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherapi}&units=metric"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        weather_desc = data['weather'][0]['description']
        if 'rain' in weather_desc.lower():
            return "Yes, rain is expected."
        else:
            return "No, rain is not expected."
    else:
        return "Sorry, I couldn't retrieve the weather information."

def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return "Sorry, I couldn't retrieve the CPU temperature."
        cpu_temp = temps.get('coretemp', [])[0].current if 'coretemp' in temps else temps[list(temps.keys())[0]][0].current
        return f"The current CPU temperature is {cpu_temp} degrees Celsius."
    except Exception as e:
        return f"Sorry, an error occurred while retrieving the CPU temperature: {e}"

def tell_joke():
    joke = pyjokes.get_joke()
    return joke

def chat_mode():
    speak("Chat mode activated. Ask me anything.")
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, phrase_time_limit=2)
            print("Recognizing...")
        try:
            query = recognizer.recognize_google(audio)
            if query.lower() == "deactivate chat mode":
                speak("Deactivating chat mode.")
                break
            elif "tell me a joke" in query.lower():
                joke = tell_joke()
                speak(joke)
            elif "tell me the temperature" in query.lower() or "what's the temperature" in query.lower():
                weather_info = get_weather()
                speak(weather_info)
            elif "tell me the cpu temperature" in query.lower() or "what's the cpu temperature" in query.lower():
                cpu_temp_info = get_cpu_temperature()
                speak(cpu_temp_info)
            elif "is rain coming" in query.lower() or "rain forecast" in query.lower():
                rain_info = get_weather()
                speak(rain_info)
            else:
                speak("Sorry, I'm still learning. I didn't understand that.")
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, I couldn't understand that.")

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("http://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("http://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("http://linkedin.com")
    elif "open chatgpt" in c.lower():
        webbrowser.open("http://chatgpt.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "tell me the news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
    elif "tell me the temperature" in c.lower() or "what's the temperature" in c.lower():
        weather_info = get_weather()
        speak(weather_info)
    elif "tell me the cpu temperature" in c.lower() or "what's the cpu temperature" in c.lower():
        cpu_temp_info = get_cpu_temperature()
        speak(cpu_temp_info)
    elif "tell me a joke" in c.lower() or "tell me the joke" in c.lower():
        joke = tell_joke()
        speak(joke)
    elif "shut down" in c.lower():
        speak("Shutting down. Goodbye!")
        sys.exit()
    elif "off laptop" in c.lower():
        speak("Shutting down the laptop. Goodbye!")
        if os.name == 'nt':  # For Windows
            os.system("shutdown /s /t 1")
        else:
            speak("This command is not supported on your operating system.")
        sys.exit()
    elif "open file" in c.lower():
        speak("Please tell me the file path.")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                file_path = recognizer.recognize_google(audio)
                if os.path.isfile(file_path):
                    os.startfile(file_path)
                    speak(f"Opening file {file_path}")
                else:
                    speak("File not found.")
            except Exception as e:
                speak(f"Sorry, an error occurred: {e}")
    elif "jarvis" in c.lower():
        speak("Turning off chat mode.")
    elif "activate chat mode" in c.lower():
        chat_mode()
    elif "deactivate chat mode" in c.lower():
        speak("Chat mode is not active right now.")
    elif "is rain coming" in c.lower() or "rain forecast" in c.lower():
        rain_info = get_weather()
        speak(rain_info)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, phrase_time_limit=4)
            print("Recognizing...")
        try:
            word = recognizer.recognize_google(audio)
            if "jarvis" in word.lower():  # Change from "jasvis" to "jarvis"
                speak("Yes boss")
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
            elif "activate chat mode" in word.lower():
                chat_mode()
            elif "deactivate chat mode" in word.lower():
                speak("Chat mode is not active right now.")
        except Exception as e:
            print(f"Error: {e}")
