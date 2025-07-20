## Here you must insert your own private keys. Follow the instructions:
## go to picovoice.ai/ > Sign In > Continue with Google > Enter your Google account > 
## Enter your first, last name and github profile > In console.picovoice.ai/ >> copy and paste the AccessKey.
## Then in the navbar, go to Porcupine > Select a language > English > Wake Word > "Hey Karen" > select the microphone icon
## After recognized, select Train > Platform > Windows (x86_64.arm64) > Select Download > Will download a .zip with a .ppn file
## Paste that .ppn file to the project folder.

## Do this procedure for each access key

PICOVOICE_ACCESS_KEY_EN = "[Insert your own]"
PICOVOICE_ACCESS_KEY_ES = "[Insert your own]"
PICOVOICE_ACCESS_KEY_ZH = "[Insert your own]"


WAKE_WORD_EN_FILE = "hey_karen_en.ppn"
WAKE_WORD_ES_FILE = "hey_karen_es.ppn"
WAKE_WORD_ZH_FILE = "ni_hao_mei_li_zh.ppn"
MODEL_ES_FILE = "porcupine_params_es.pv"
MODEL_ZH_FILE = "porcupine_params_zh.pv"
KAREN_PIC_FILE = "karenPic.jpeg"
KAREN_CIRCLE_PIC_FILE = "karenCirclePic.png"
ROBOTO_FONT_FILE = "Roboto-Regular.ttf"


MESSAGES = {
    'en': {
        "listening": "\nListening for your command...",
        "unintelligible": "\nSorry, I did not understand that.",
        "service_down": "\nSorry, my speech service is down.",
        "playing_youtube": "\nPlaying {} on YouTube...",
        "ask_youtube": "\nWhat video would you like me to play?",
        "searching_google": "\nSearching Google for: {}",
        "ask_search": "\nWhat would you like to search for?",
        "unrecognized": "\nCommand not recognized.",
        "wake_detected": "\nWake word detected!",
        "timer_set": "\nOkay, setting a timer for {} minutes.",
        "timer_done": "\nYour timer is up!",
        "timer_no_number": "\nSorry, I couldn't determine the duration for the timer."
    },
    'es': {
        "listening": "\nEscuchando tu comando...",
        "unintelligible": "\nDisculpa, no entendí eso.",
        "service_down": "\nDisculpa, el servicio de voz no está disponible.",
        "playing_youtube": "\nReproduciendo {} en YouTube...",
        "ask_youtube": "\n¿Qué video te gustaría reproducir?",
        "searching_google": "\nBuscando en Google: {}",
        "ask_search": "\n¿Qué te gustaría buscar?",
        "unrecognized": "\nComando no reconocido.",
        "wake_detected": "\n¡Palabra de activación detectada!",
        "timer_set": "\nOk, iniciando un temporizador de {} minutos.",
        "timer_done": "\n¡Se acabó el tiempo!",
        "timer_no_number": "\nDisculpa, no pude determinar la duración del temporizador."
    },
    'zh': {
        "listening": "\n正在聆听您的命令...",
        "unintelligible": "\n抱歉，我没听清。",
        "service_down": "\n抱歉，语音服务暂不可用。",
        "playing_youtube": "\n正在YouTube上播放{}...",
        "ask_youtube": "\n您想看哪个视频?",
        "searching_google": "\n正在Google中搜索：{}",
        "ask_search": "\n您想搜索什么？",
        "unrecognized": "\n无法识别该命令。",
        "wake_detected": "\n我听到了！",
        "timer_set": "\n好的，{}分钟的计时器已设定。",
        "timer_done": "\n时间到！",
        "timer_no_number": "\n抱歉，未能确定计时时长。"
    }
}
