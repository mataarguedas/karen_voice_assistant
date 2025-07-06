import datetime
import geocoder
import os
import pyaudio
import pyautogui
import pyttsx3
import pywhatkit
import pvporcupine
import re
import speech_recognition as sr
import struct
import sys
import threading
import time
import webbrowser

def display_splash_screen():
    try:
        clear_screen()
        print("\n\n")
        print("\t\t\t\t\t ##   ##   ###   #####   #######       #####  ##   ##   ")
        time.sleep(0.06)
        print("\t\t\t\t\t ### ###  ## ##  ##  ##  ##            ##  ##  ## ##    ")
        time.sleep(0.06)
        print("\t\t\t\t\t ####### ##  ##  ##   ## ##            ##  ##   ###     ")
        time.sleep(0.06)
        print("\t\t\t\t\t ## # ## ##  ##  ##   ## ######        #####     #      ")
        time.sleep(0.06)
        print("\t\t\t\t\t ##   ## ######  ##  ##  ##            ##  ##    #      ")
        time.sleep(0.06)
        print("\t\t\t\t\t ##   ## ##  ##  ##  ##  ##            ##  ##    #      ")
        time.sleep(0.06)
        print("\t\t\t\t\t ##   ## ##  ##  #####   #######       #####     #      \n")
        time.sleep(0.1)

        print("                                #######  ##   ##  ##   ##   ###    ##   ##  ##  ##  #######  ##      ")
        time.sleep(0.06)
        print("                                ##       ### ###  ##   ##  ## ##   ###  ##  ##  ##  ##       ##      ")
        time.sleep(0.06)
        print("                                ######   #######  ####### ##   ##  #### ##  ##  ##  ######   ##      ")
        time.sleep(0.06)
        print("                                ##       ## # ##  ## # ## #######  ## ####  ##  ##  ##       ##      ")
        time.sleep(0.06)
        print("                                ##       ##   ##  ##   ## ##   ##  ##  ###  ##  ##  ##       ##      ")
        time.sleep(0.06)
        print("                                #######  ##   ##  ##   ## ##   ##  ##   ##   #####  #######  ####### \n")
        time.sleep(2)
        print("                                                      Emmanuel's S&Hware.")
        time.sleep(2)
        print("                                        Providing your Software and Hardware since 2025.")
        time.sleep(2.5)
    except KeyboardInterrupt:
        print("\nSplash screen skipped.")
        sys.exit()

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

PICOVOICE_ACCESS_KEY_EN = "eRoIXftBuShCDzkiVx+89w9KpO7fQkUMDDSXA3qcCXLD53HAC1FVjw=="
PICOVOICE_ACCESS_KEY_ES = "eYwmeuJKw4e45Yk70luJMEn3BqInhw6tqo41aFkmEtHLE5u3+R4z1Q=="

WAKE_WORD_PATH_EN = resource_path("hey_karen_en.ppn")
WAKE_WORD_PATH_ES = resource_path("hey_karen_es.ppn")
MODEL_PATH_ES = resource_path("porcupine_params_es.pv")

MESSAGES = {
    'en': {
        "listening": "Listening for your command...",
        "unintelligible": "Sorry, I did not understand that.",
        "service_down": "Sorry, my speech service is down.",
        "playing_youtube": "Playing {} on YouTube...",
        "ask_youtube": "What video would you like me to play?",
        "searching_google": "Searching Google for: {}",
        "ask_search": "What would you like me to search for?",
        "unrecognized": "Command not recognized.",
        "wake_detected": "Wake word detected! Listening for your command...",
        "timer_set": "Okay, setting a timer for {} minutes.",
        "timer_done": "Your timer is up!",
        "timer_no_number": "Sorry, I couldn't determine the duration for the timer."
    },
    'es': {
        "listening": "Escuchando tu comando...",
        "unintelligible": "Disculpa, no entendí eso.",
        "service_down": "Disculpa, el servicio de voz no está disponible.",
        "playing_youtube": "Reproduciendo {} en YouTube...",
        "ask_youtube": "¿Qué video te gustaría reproducir?",
        "searching_google": "Buscando en Google: {}",
        "ask_search": "¿Qué te gustaría buscar?",
        "unrecognized": "Comando no reconocido.",
        "wake_detected": "¡Palabra de activación detectada! Escuchando tu comando...",
        "timer_set": "Ok, iniciando un temporizador de {} minutos.",
        "timer_done": "¡Se acabó el tiempo!",
        "timer_no_number": "Disculpa, no pude determinar la duración del temporizador."
    }
}

tts_engine = pyttsx3.init()
def speak(text, lang_choice='en'):
    print(f"Karen: {text}")
    try:
        if lang_choice == 'es':
            voices = tts_engine.getProperty('voices')
            es_voice = next((v for v in voices if 'spanish' in v.name.lower()), None)
            if es_voice:
                tts_engine.setProperty('voice', es_voice.id)
    except Exception:
        pass
    tts_engine.say(text)
    tts_engine.runAndWait()

def set_timer(duration_minutes, lang_choice='en'):
    
    def timer_finished():
        speak(MESSAGES[lang_choice]['timer_done'], lang_choice)

    try:
        duration_seconds = int(duration_minutes) * 60
        speak(MESSAGES[lang_choice]['timer_set'].format(duration_minutes), lang_choice)
        

        timer_thread = threading.Timer(duration_seconds, timer_finished)
        timer_thread.daemon = True
        timer_thread.start()

    except ValueError:
        speak(MESSAGES[lang_choice]['timer_no_number'], lang_choice)

def get_current_time(lang_choice='en'):
    now = datetime.datetime.now()
    if lang_choice == 'es':
        return now.strftime("La hora es %I:%M %p")
    else:
        return now.strftime("The time is %I:%M %p")

def get_current_date(lang_choice='en'):
    now = datetime.datetime.now()
    def suffix(d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
    day = now.day
    if lang_choice == 'es':
        formatted_date = now.strftime(f"Hoy es %A, %d de %B de %Y")
    else:
        day_with_suffix = f"{day}{suffix(day)}"
        formatted_date = now.strftime(f"Today is %A, %B {day_with_suffix}, %Y")

    return formatted_date

def get_current_location():
    g = geocoder.ip('me')
    return g.country

def listen_for_command(language_code='en-US', lang_choice='en'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(MESSAGES[lang_choice]["listening"])
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language=language_code).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak(MESSAGES[lang_choice]["unintelligible"], lang_choice)
        return None
    except sr.RequestError:
        speak(MESSAGES[lang_choice]["service_down"], lang_choice)
        return None

def search_google(query, lang_choice='en'):
    speak(MESSAGES[lang_choice]["searching_google"].format(query), lang_choice)
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def play_on_youtube(video_name, lang_choice='en'):
    """
    Plays a video on YouTube, waits for it to load, clicks the window to focus, 
    and then presses spacebar to play.
    """
    try:
        speak(MESSAGES[lang_choice]["playing_youtube"].format(video_name), lang_choice)
        pywhatkit.playonyt(video_name)
        
        print("Waiting for YouTube to load...")
        time.sleep(3) 
        
        pyautogui.click(pyautogui.size().width / 2, pyautogui.size().height / 2)
        time.sleep(0.5) 
        print("Play command sent.")

    except Exception as e:
        print(f"An error occurred with the YouTube function: {e}")

def process_command(command, lang_choice='en'):
    if command is None:
        return

    timer_en_pattern = r"set a timer for (\d+) minutes"
    timer_es_pattern = r"pon un temporizador de (\d+) minutos"
    
    match_en = re.search(timer_en_pattern, command)
    match_es = re.search(timer_es_pattern, command)

    if match_en and lang_choice == 'en':
        minutes = match_en.group(1)
        set_timer(minutes, lang_choice)
    elif match_es and lang_choice == 'es':
        minutes = match_es.group(1)
        set_timer(minutes, lang_choice)

    if ("what time is it" in command and lang_choice == 'en') or ("qué hora es" in command and lang_choice == 'es'):
        speak(get_current_time(lang_choice), lang_choice)
    elif ("what's the date" in command and lang_choice == 'en') or ("qué día es hoy" in command and lang_choice == 'es'):
        speak(get_current_date(lang_choice), lang_choice)
    elif ("where are we" in command and lang_choice == 'en') or ("dónde estamos" in command and lang_choice == 'es'):
        response = "We are in " + get_current_location() if lang_choice == 'en' else "Estamos en " + get_current_location()
        speak(response, lang_choice)
    elif ("search for" in command and lang_choice == 'en') or ("busca" in command and lang_choice == 'es'):
        query = command.split("search for" if lang_choice == 'en' else "busca", 1)[1].strip()
        if query:
            search_google(query, lang_choice)
        else:
            speak(MESSAGES[lang_choice]["ask_search"], lang_choice)
    elif (("play" in command and "on youtube" in command) and lang_choice == 'en') or \
         (("reproduce" in command and "en youtube" in command) and lang_choice == 'es'):
        if lang_choice == 'en':
            video_name = command.split("play", 1)[1].split("on youtube", 1)[0].strip()
        else:
            video_name = command.split("reproduce", 1)[1].split("en youtube", 1)[0].strip()
        if video_name:
            play_on_youtube(video_name, lang_choice)
        else:
            speak(MESSAGES[lang_choice]["ask_youtube"], lang_choice)
    else:
        speak(MESSAGES[lang_choice]["unrecognized"], lang_choice)



if __name__ == "__main__":
    display_splash_screen()
    clear_screen()

    porcupine_en = None
    porcupine_es = None
    pa = None
    audio_stream = None

    try:
        porcupine_en = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY_EN,
            keyword_paths=[WAKE_WORD_PATH_EN]
        )
        porcupine_es = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY_ES,
            keyword_paths=[WAKE_WORD_PATH_ES],
            model_path=MODEL_PATH_ES
        )
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine_en.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine_en.frame_length
        )
        print("Listening for a wake word ('Hey Karen' or 'Ey Karen')...")
        while True:
            pcm = audio_stream.read(porcupine_en.frame_length)
            pcm = struct.unpack_from("h" * porcupine_en.frame_length, pcm)
            keyword_index_en = porcupine_en.process(pcm)
            keyword_index_es = porcupine_es.process(pcm)
            if keyword_index_en == 0:
                lang_code = 'en-US'
                lang_choice = 'en'
                print(f"\n--- {MESSAGES[lang_choice]['wake_detected']} ---")
                command_text = listen_for_command(language_code=lang_code, lang_choice=lang_choice)
                process_command(command_text, lang_choice=lang_choice)
                print("\nListening for a wake word ('Hey Karen' or 'Ey Karen')...")
            elif keyword_index_es == 0:
                lang_code = 'es-CR'
                lang_choice = 'es'
                print(f"\n--- {MESSAGES[lang_choice]['wake_detected']} ---")
                command_text = listen_for_command(language_code=lang_code, lang_choice=lang_choice)
                process_command(command_text, lang_choice=lang_choice)
                print("\nListening for a wake word ('Hey Karen' or 'Ey Karen')...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        if porcupine_en is not None:
            porcupine_en.delete()
        if porcupine_es is not None:
            porcupine_es.delete()