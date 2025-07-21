Karen - A Personal Voice Assistant

A desktop voice assistant with a clean graphical user interface built using Python. Karen listens for a wake word, responds to commands on English, Spanish and Mandarin, and provides visual feedback for an interactive experience.

Features

    Trilingual Support: Fully functional in English, Spanish, and Mandarin, from wake word to command processing.

    Wake Word Detection: Utilizes the powerful and lightweight Porcupine wake word engine to listen for "Hey Karen" (English), "Ey Karen" (Spanish) or "Nǐ hǎo měi lì" (你好美丽) （Mandarin）.

    Core Voice Commands:

        Time & Date: Get the current time and date.

        Location: Instantly find out your current country.

        Timers: Set timers with simple voice commands.

        Web Search: Search for anything on Google.

        YouTube Integration: Play your favorite videos directly on YouTube.

    Graphical User Interface (GUI): A sleek and modern UI built with PyQt5 that displays a log of interactions and provides a circular visual indicator that animates when Karen is actively listening.

    Text-to-Speech Feedback: Karen communicates back, confirming actions and delivering information clearly.

Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites

    Python 3.8+

    A Picovoice Access Key. You can get one for free from the Picovoice Console.

    For some operating systems, PyAudio requires the portaudio library to be installed.

        On Debian/Ubuntu: sudo apt-get install portaudio19-dev

        On macOS (using Homebrew): brew install portaudio
        
    A Mandarin text-to-speech (TTS) voice pack installed on your operating system for Mandarin voice output.

Installation

    The easy-peasy-sneaky-peaky-lemon-squeezy way, download karen.exe and run it.

    Nevertheless, the hardy-farty-chili-spicy way:
    
    1. Clone the Repository
    git clone https://github.com/your-username/karen-voice-assistant.git
    cd karen-voice-assistant

    2. Project Structure
    Ensure all the necessary asset files are placed in the root directory of the project alongside the script. The application depends on these files to function correctly.
    
    /karen-voice-assistant
    ├── main.py                 # Main application entry point
    ├── config.py               # Configuration for API keys and file paths
    ├── requirements.txt        # List of project dependencies
    │
    ├── backend/
    │   └── voice_assistant.py  # Handles wake word, speech recognition, and command processing
    │
    ├── ui/
    │   └── main_window.py      # Defines the PyQt5 graphical user interface
    │
    ├── utils/
    │   └── helpers.py          # Utility functions, like handling resource paths
    │
    └── assets/
        ├── hey_karen_en.ppn        # English wake word model
        ├── hey_karen_es.ppn        # Spanish wake word model
        ├── ni_hao_mei_li_zh.ppn    # Mandarin wake word model
        ├── porcupine_params_es.pv  # Porcupine Spanish language model
        ├── porcupine_params_zh.pv  # Porcupine Mandarin language model
        ├── karenCirclePic.png      # Application icon
        └── voice_indicator.png     # Image for the animated voice indicator

    3. Set Up a Virtual Environment
    It is highly recommended to use a virtual environment to manage dependencies and avoid conflicts.

    # Create the virtual environment
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

    4. Install Dependencies
    A requirements.txt file is included to simplify the installation of all required Python libraries.

        requirements.txt:
          PyQt5
          pvporcupine
          pyaudio
          pyautogui
          pyttsx3
          pywhatkit
          SpeechRecognition
          geocoder
          Pillow

    Installation command:
    pip install -r requirements.txt

    5. Configure API Keys
    Open the config.py script and insert your Picovoice Access Key(s) into the Backend class.
    # in config.py:
    class Backend(QObject):
        def __init__(self):
            super().__init__()
            # Replace these placeholder strings with your actual key
            PICOVOICE_ACCESS_KEY_EN = "YOUR_PICOVOICE_ACCESS_KEY"
            PICOVOICE_ACCESS_KEY_ES = "YOUR_PICOVOICE_ACCESS_KEY"
            PICOVOICE_ACCESS_KEY_ZH = "YOUR_PICOVOICE_ACCESS_KEY"

Usage
    
    After completing the installation, you can launch the application by running the main script from your terminal:
    python karen_ui.py

    The application window will appear, and Karen will be passively listening for the wake word.

    Voice Commands
    Activate Karen with the wake word ("Hey Karen" or "Ey Karen") and then issue one of the following commands:

      1. "What time is it?",  "¿Qué hora es?" or " "现在几点" (xiàn zài jǐ diǎn)" tells you the current time.
      2. "What's the date?", "¿Qué día es hoy?" or " "今天几号" (jīn tiān jǐ hào)" tells you the current date.
      3. "Where are we?", "¿Dónde estamos?" or " "我们在哪" (wǒ men zài nǎ'er)" identifies your current country via your IP.
      4. "Set a timer for X minutes", "Pon un temporizador de X minutos" or " "设置一个 X分钟的计时器"(Shèzhì yīgè X fēnzhōng de jìshí qì)" sets a timer for the specified X minutes.
      5. "Search for ____________________", "Busca ____________________" or ""搜索 ____________________" (sōu suǒ ____________________)" opens a new browser tab with Google search results.
      6. "Play ____________________ on YouTube" or "Reproduce ____________________ en YouTube" or " 播放 ____________________ 在youtube上" (bō fàng ____________________ zài youtube shàng) " finds and plays the requested video on YouTube.

License
    
    This project is distributed under the MIT License. See the LICENSE.md file for more details.
    
Acknowledgments
    
    A big thank you to Picovoice for providing the accurate and efficient Porcupine wake word engine.
    This assistant uses the Google Speech Recognition API via the versatile SpeechRecognition library.
