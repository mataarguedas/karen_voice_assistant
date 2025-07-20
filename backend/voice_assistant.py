import datetime
import geocoder
import os
import pvporcupine
import pyaudio
import pyautogui
import pyttsx3
import pywhatkit
import re
import speech_recognition as sr
import struct
import threading
import time
import webbrowser

from PyQt5.QtCore import QObject, pyqtSignal

import config
from utils.helpers import resource_path

class VoiceAssistant(QObject):
    update_text = pyqtSignal(str)
    voice_activity = pyqtSignal(bool)
    wake_word_detected = pyqtSignal()
    command_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._is_running = True
        self._load_paths()

    def _load_paths(self):
        self.WAKE_WORD_PATH_EN = resource_path(config.WAKE_WORD_EN_FILE)
        self.WAKE_WORD_PATH_ES = resource_path(config.WAKE_WORD_ES_FILE)
        self.WAKE_WORD_PATH_ZH = resource_path(config.WAKE_WORD_ZH_FILE)
        self.MODEL_PATH_ES = resource_path(config.MODEL_ES_FILE)
        self.MODEL_PATH_ZH = resource_path(config.MODEL_ZH_FILE)

        paths_to_check = {
            "English wake word": self.WAKE_WORD_PATH_EN,
            "Spanish wake word": self.WAKE_WORD_PATH_ES,
            "Chinese wake word": self.WAKE_WORD_PATH_ZH,
            "Spanish model": self.MODEL_PATH_ES,
            "Chinese model": self.MODEL_PATH_ZH
        }

        for name, path in paths_to_check.items():
            if not os.path.exists(path):
                self.update_text.emit(f"ERROR: {name} file not found at {path}")
            else:
                self.update_text.emit(f"OK: Found {name} file.")


    def stop(self):
        self._is_running = False

    def speak_in_thread(self, text, lang_choice):
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            if lang_choice == 'es':
                es_voice = next((v for v in voices if 'spanish' in v.name.lower()), None)
                if es_voice: engine.setProperty('voice', es_voice.id)
            elif lang_choice == 'zh':
                zh_voice = next((v for v in voices if 'chinese' in v.name.lower()), None)
                if zh_voice: engine.setProperty('voice', zh_voice.id)

            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            self.update_text.emit(f"TTS Error: {e}")

    def speak(self, text, lang_choice='en'):
        if text == config.MESSAGES[lang_choice]["wake_detected"]:
            return
        self.update_text.emit(f"\nKaren: {text}")
        threading.Thread(target=self.speak_in_thread, args=(text, lang_choice), daemon=True).start()

    def listen_for_command(self, language_code='en-US', lang_choice='en'):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                self.update_text.emit(config.MESSAGES[lang_choice]["listening"])
                self.voice_activity.emit(True)
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                self.voice_activity.emit(False)
            
            command = r.recognize_google(audio, language=language_code).lower()
            self.update_text.emit(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            self.update_text.emit("Listening timeout - no speech detected")
            self.voice_activity.emit(False)
            return None
        except sr.UnknownValueError:
            self.speak(config.MESSAGES[lang_choice]["unintelligible"], lang_choice)
            return None
        except sr.RequestError:
            self.speak(config.MESSAGES[lang_choice]["service_down"], lang_choice)
            return None
        except Exception as e:
            self.update_text.emit(f"Speech recognition error: {e}")
            self.voice_activity.emit(False)
            return None

    def process_command(self, command, lang_choice='en'):
        if command is None:
            return

        timer_en_pattern = r"set a timer for (\d+) minutes"
        timer_es_pattern = r"pon un temporizador de (\d+) minutos"
        timer_zh_pattern = r"设置一个(\d+)分钟的计时器"
        
        match_en = re.search(timer_en_pattern, command)
        match_es = re.search(timer_es_pattern, command)
        match_zh = re.search(timer_zh_pattern, command)

        if match_en and lang_choice == 'en': self.set_timer(match_en.group(1), lang_choice)
        elif match_es and lang_choice == 'es': self.set_timer(match_es.group(1), lang_choice)
        elif match_zh and lang_choice == 'zh': self.set_timer(match_zh.group(1), lang_choice)
        elif ("what time is it" in command and lang_choice == 'en') or ("qué hora es" in command and lang_choice == 'es') or ("现在几点" in command and lang_choice == 'zh'): self.speak(self.get_current_time(lang_choice), lang_choice)
        elif ("what's the date" in command and lang_choice == 'en') or ("qué día es hoy" in command and lang_choice == 'es') or ("今天几号" in command and lang_choice == 'zh'): self.speak(self.get_current_date(lang_choice), lang_choice)
        elif ("where are we" in command and lang_choice == 'en') or ("dónde estamos" in command and lang_choice == 'es') or ("我们在哪" in command and lang_choice == 'zh'):
            location = self.get_current_location()
            if lang_choice == 'en': self.speak(f"We are in {location}", lang_choice)
            elif lang_choice == 'es': self.speak(f"Estamos en {location}", lang_choice)
            elif lang_choice == 'zh': self.speak(f"我们在{location}", lang_choice)
        elif ("search for" in command and lang_choice == 'en') or ("busca" in command and lang_choice == 'es') or ("搜索" in command and lang_choice == 'zh'):
            query_keyword = {"en": "search for", "es": "busca", "zh": "搜索"}[lang_choice]
            query = command.split(query_keyword, 1)[1].strip()
            if query: self.search_google(query, lang_choice)
            else: self.speak(config.MESSAGES[lang_choice]["ask_search"], lang_choice)
        elif (("play" in command and "on youtube" in command) and lang_choice == 'en') or (("reproduce" in command and "en youtube" in command) and lang_choice == 'es') or (("播放" in command and ("在youtube上" in command or "在油管上" in command)) and lang_choice == 'zh'):
            if lang_choice == 'en': video_name = command.split("play", 1)[1].split("on youtube", 1)[0].strip()
            elif lang_choice == 'es': video_name = command.split("reproduce", 1)[1].split("en youtube", 1)[0].strip()
            elif lang_choice == 'zh': video_name = command.split("播放", 1)[1].split("在youtube上" if "在youtube上" in command else "在油管上", 1)[0].strip()
            if video_name: self.play_on_youtube(video_name, lang_choice)
            else: self.speak(config.MESSAGES[lang_choice]["ask_youtube"], lang_choice)
        else:
            self.speak(config.MESSAGES[lang_choice]["unrecognized"], lang_choice)
    
    # ... (All other methods from Backend class: set_timer, get_current_time, etc.) ...
    def set_timer(self, duration_minutes, lang_choice='en'):
        def timer_finished(): self.speak(config.MESSAGES[lang_choice]['timer_done'], lang_choice)
        try:
            threading.Timer(int(duration_minutes) * 60, timer_finished).start()
            self.speak(config.MESSAGES[lang_choice]['timer_set'].format(duration_minutes), lang_choice)
        except ValueError: self.speak(config.MESSAGES[lang_choice]['timer_no_number'], lang_choice)

    def get_current_time(self, lang_choice='en'):
        if lang_choice == 'zh': return datetime.datetime.now().strftime("现在是 %p %I 点 %M 分")
        return datetime.datetime.now().strftime("The time is %I:%M %p" if lang_choice == 'en' else "La hora es %I:%M %p")

    def get_current_date(self, lang_choice='en'):
        now = datetime.datetime.now()
        if lang_choice == 'es': return now.strftime(f"Hoy es %A, %d de %B de %Y")
        if lang_choice == 'zh': return now.strftime("今天是%Y年%m月%d日, 星期%A").replace('Sunday','日').replace('Monday','一').replace('Tuesday','二').replace('Wednesday','三').replace('Thursday','四').replace('Friday','五').replace('Saturday','六')
        def suffix(d): return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
        return now.strftime(f"Today is %A, %B {now.day}{suffix(now.day)}, %Y")

    def get_current_location(self): return geocoder.ip('me').country
    def search_google(self, q, l): self.speak(config.MESSAGES[l]["searching_google"].format(q),l); webbrowser.open(f"https://google.com/search?q={q.replace(' ','+')}")
    def play_on_youtube(self, v, l):
        try:
            self.speak(config.MESSAGES[l]["playing_youtube"].format(v),l); pywhatkit.playonyt(v); time.sleep(3); pyautogui.click(pyautogui.size().width/2, pyautogui.size().height/2)
        except Exception as e: self.update_text.emit(f"YouTube Error: {e}")

    def run(self):
        porcupine_en, porcupine_es, porcupine_zh, pa, audio_stream = None, None, None, None, None
        try:
            while self._is_running:
                try:
                    porcupine_en = pvporcupine.create(access_key=config.PICOVOICE_ACCESS_KEY_EN, keyword_paths=[self.WAKE_WORD_PATH_EN])
                    porcupine_es = pvporcupine.create(access_key=config.PICOVOICE_ACCESS_KEY_ES, keyword_paths=[self.WAKE_WORD_PATH_ES], model_path=self.MODEL_PATH_ES)
                    porcupine_zh = pvporcupine.create(access_key=config.PICOVOICE_ACCESS_KEY_ZH, keyword_paths=[self.WAKE_WORD_PATH_ZH], model_path=self.MODEL_PATH_ZH)
                    
                    pa = pyaudio.PyAudio()
                    audio_stream = pa.open(rate=porcupine_en.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine_en.frame_length)
                    
                    while self._is_running:
                        pcm = audio_stream.read(porcupine_en.frame_length, exception_on_overflow=False)
                        pcm = struct.unpack_from("h" * porcupine_en.frame_length, pcm)
                        
                        lang_choice = None
                        if porcupine_en.process(pcm) >= 0: lang_choice = 'en'
                        elif porcupine_es.process(pcm) >= 0: lang_choice = 'es'
                        elif porcupine_zh.process(pcm) >= 0: lang_choice = 'zh'
                        
                        if lang_choice:
                            self.wake_word_detected.emit()
                            if audio_stream: audio_stream.stop_stream(); audio_stream.close()
                            if pa: pa.terminate()
                            if porcupine_en: porcupine_en.delete()
                            if porcupine_es: porcupine_es.delete()
                            if porcupine_zh: porcupine_zh.delete()
                            audio_stream, pa, porcupine_en, porcupine_es, porcupine_zh = None, None, None, None, None
                            
                            lang_code = {'en': 'en-US', 'es': 'es-CR', 'zh': 'zh-CN'}[lang_choice]
                            self.update_text.emit(f"\n {config.MESSAGES[lang_choice]['wake_detected']} \n")
                            time.sleep(0.1)
                            command = self.listen_for_command(language_code=lang_code, lang_choice=lang_choice)
                            
                            self.command_finished.emit()
                            time.sleep(0.2)
                            
                            self.process_command(command, lang_choice=lang_choice)
                            break
                except Exception as e:
                    self.update_text.emit(f"Audio processing error: {e}")
                    time.sleep(0.1)
                finally:
                    if audio_stream:
                        try: audio_stream.stop_stream(); audio_stream.close()
                        except: pass
                    if pa:
                        try: pa.terminate()
                        except: pass
                    if porcupine_en: porcupine_en.delete()
                    if porcupine_es: porcupine_es.delete()
                    if porcupine_zh: porcupine_zh.delete()
                    audio_stream, pa, porcupine_en, porcupine_es, porcupine_zh = None, None, None, None, None
        except Exception as e:
            self.update_text.emit(f"A critical error occurred: {e}")

