# https://www.ibm.com/demos/live/tts-demo/self-service/home     Alison, high pitch, 0.9 speed (Audacity)
# autohotkey
try:
    import time
    import random
    import simpleaudio as sa
    import speech_recognition as sr
    import threading
    import subprocess
    import webbrowser

except ImportError:
    import time
    import random
    import simpleaudio as sa
    import speech_recognition as sr
    import threading
    import subprocess
    import webbrowser


# The assistant's name is LoLa
def speech_input(timeout_limit):

    with mic:

        print('Say a command')
        print(f'Current timeout is {timeout_limit}')
        try:
            audio = recognizer.listen(mic, timeout=timeout_limit, phrase_time_limit=timeout_limit)

        except sr.WaitTimeoutError:
            return 'none'

        try:
            print("Processing...\n")
            voice_to_text = recognizer.recognize_google(audio).lower()

        except sr.UnknownValueError:
            return 'none'

        except sr.RequestError:
            return 'none'

    return voice_to_text.lower()


def tts_voice(file_path):

    # Function to call a wav file as Lola's voice
    wav_path = sa.WaveObject.from_wave_file(file_path)
    play_wav = wav_path.play()
    play_wav.wait_done()


def thread_starter(argument):

    try:
        # Used a lambda function instead of creating a named function to execute the autohotkey voices inside of
        # the thread function
        thread = threading.Thread(target=lambda: subprocess.call(argument))
        thread.daemon = True
        thread.start()

    except FileNotFoundError:
        print("file not found")
        thread_starter(argument)

    except FileExistsError:
        print("file not found")
        thread_starter(argument)


def league_client(execute):

    # Threading is used in accept and decline game for speeding up as there is a time limit
    # TTS sometimes picks up except instead of accept
    if execute == 'accept game' or execute == 'except game':
        thread_starter('ahk/Accept game.exe')
        accept = threading.Thread(target=lambda: tts_voice('tts/Game accepted.wav'))
        accept.daemon = True
        accept.start()

    elif 'decline game' in execute:
        thread_starter('ahk/Decline game.exe')
        decline = threading.Thread(target=lambda: tts_voice('tts/Game declined.wav'))
        decline.daemon = True
        decline.start()

    elif 'set as away' in execute or 'set as online' in execute:
        thread_starter('ahk/Set as away or online.exe')

        if 'set as away' in execute:
            tts_voice('tts/Set as away.wav')

        elif 'set as online' in execute:
            tts_voice('tts/Set as online.wav')

    elif 'accept invite' in execute or 'except invite' in execute:
        tts_voice('tts/Yes sir.wav')
        thread_starter('ahk/Accept invite.exe')

    elif 'decline invite' in execute:
        thread_starter('ahk/Decline invite.exe')
        tts_voice('tts/Yes sir.wav')

    elif 'search for a game' in execute or 'find match' in execute or 'search' in execute:
        thread_starter('ahk/Find match.exe')
        tts_voice('tts/Yes sir.wav')

    elif 'cancel search' in execute:
        thread_starter('ahk/Cancel find match.exe')
        tts_voice('tts/Yes sir.wav')

    elif 'create normal game' in execute or 'create normals' in execute:
        thread_starter('ahk/Create normals.exe ')
        tts_voice('tts/Yes sir.wav')

    elif 'create ranked game' in execute or 'create ranked' in execute:
        thread_starter('ahk/Create Ranked.exe')
        tts_voice('tts/Yes sir.wav')

    elif 'create flex game' in execute:
        thread_starter('ahk/Create flex.exe')
        tts_voice('tts/Yes sir.wav')

    elif 'create a all random' in execute or 'create all random' in execute:
        thread_starter('ahk/Create aram.exe')
        tts_voice('tts/Yes sir.wav')

    elif 'change game mode' in execute:
        thread_starter('ahk/Change game mode.exe')
        tts_voice('tts/Yes sir.wav')

    # If it the keywords primary or secondary role is in the string, it will call the function accordingly
    elif 'set primary role' in execute:
        tts_voice('tts/Setting primary.wav')
        primary_role = threading.Thread(target=primary_lanes, args=(execute,))
        primary_role.daemon = True
        primary_role.start()

    elif 'set secondary role' in execute:
        tts_voice('tts/Setting secondary.wav')
        secondary_role = threading.Thread(target=secondary_lane, args=(execute,))
        secondary_role.daemon = True
        secondary_role.start()

    elif 'set role as' in execute:
        pass


# The positions of the primary and secondary roles differ in the client, hence 2 separate functions
def primary_lanes(lane):

    if 'mid' in lane:
        thread_starter('ahk/Mid lane (1)')

    elif 'bot' in lane or 'bottom':
        thread_starter('ahk/Bot lane (1)')

    elif 'support' in lane:
        thread_starter('ahk/Support lane (1)')

    elif 'top' in lane:
        thread_starter('ahk/Top lane (1)')

    elif 'jungle' in lane:
        thread_starter('ahk/Jungle lane (1)')

    elif 'fill' in lane:
        thread_starter('ahk/Fill lane (1)')


def secondary_lane(lane):

    if 'mid' in lane:
        thread_starter('ahk/Mid lane (2)')

    elif 'bot' in lane or 'bottom':
        thread_starter('ahk/Bot lane (2)')

    elif 'support' in lane:
        thread_starter('ahk/Support lane (2)')

    elif 'top' in lane:
        thread_starter('ahk/Top lane (2)')

    elif 'jungle' in lane:
        thread_starter('ahk/Jungle lane (2)')

    elif 'fill' in lane:
        thread_starter('ahk/Fill lane (2)')


def execute_work(execute):

    if 'google' in execute:
        tts_voice('tts/Opening Google.wav')
        google = execute.split('google ')[1].lower()
        webbrowser.open('https://www.google.com/search?q=' + google, new=1)

    elif 'youtube' in execute:
        tts_voice('tts/Opening Youtube.wav')
        youtube = execute.split('for ')[1].lower()
        webbrowser.open('https://www.youtube.com/results?search_query=' + youtube)

    elif 'open website at' in execute:
        tts_voice('tts/Yes sir.wav')
        browser = execute.split('at ')[1].lower()
        webbrowser.open(f'www.{browser}')

    elif execute == 'open notepad':
        subprocess.call('notepad.exe')
        tts_voice("tts/Yes sir.wav")

    elif execute == 'close notepad':
        subprocess.call('taskkill /F /IM notepad.exe')
        tts_voice("tts/Yes sir.wav")

    elif execute == 'open firefox':
        subprocess.call('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
        tts_voice("tts/Yes sir.wav")

    elif execute == 'open whatsapp':
        subprocess.call('C:\\Users\\Marcel\\AppData\\Local\\WhatsApp\\WhatsApp.exe')
        tts_voice("tts/Yes sir.wav")

    elif execute == 'play music':
        tts_voice("tts/Getting playlist.wav")
        music_list = ['https://www.youtube.com/watch?v=Ud08fMq13ok&list=RDUd08fMq13ok&start_radio=1',
                      'https://www.youtube.com/watch?v=IN39a6aYEnw&list=RDMMIN39a6aYEnw&start_radio=1',
                      'https://www.youtube.com/watch?v=eH4F1Tdb040&list=RDeH4F1Tdb040&start_radio=1']

        webbrowser.open(random.choice(music_list))

    elif 'watch list' in execute:
        webbrowser.open('https://9anime.to/user/watchlist')
        tts_voice("tts/Yes sir.wav")

    elif execute == 'open riot client':
        subprocess.call('C:\\Riot Games\\Riot Client\\RiotClientServices.exe')
        tts_voice("tts/Yes sir.wav")


time.sleep(1)
tts_voice('tts/Greeting.wav')

print("Calibrating voice recognition")

recognizer = sr.Recognizer()
with sr.Microphone() as mic:
    # recognizer.adjust_for_ambient_noise(mic, duration=4)
    # recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 380

timeout = 60

while True:

    speech = speech_input(timeout)

    print(speech)

    if 'set limit to' in speech:
        set_timeout = speech.split('to ')[1]
        timeout = int(set_timeout.strip())
        print(f'setting timeout to {timeout}')

    if 'set threshold to' in speech:
        set_threshold = speech.split('to ')[1]
        recognizer.energy_threshold = int(set_threshold)
        print(set_threshold)

    if 'thanks lola you may go' in speech or 'lola go take a nap' in speech:
        tts_voice('tts/Yuki out.wav')
        exit()

    if 'lola' in speech:

        try:
            command = speech.split('lola ')[1]

        except IndexError:
            continue

        # Created separate thread so that the execution run separately from main thread, and stays open even
        # after
        # closing main python script
        # Needs tuple (comma) for args
        # Set to daemon thread so program can fully close when exit() is called
        windows_command = threading.Thread(target=execute_work, args=(command,))
        windows_command.daemon = True
        windows_command.start()

        league_command = threading.Thread(target=league_client, args=(command,))
        league_command.daemon = True
        league_command.start()

# Return something from a threaded function
# https://www.youtube.com/watch?v=7Z-HqQSuQYc
#
# Web browser module
# https://stackoverflow.com/questions/31715119/how-can-i-open-a-website-in-my-web-browser-using-python
#
# Adjust noise level in speech recognition
# https://www.codesofinterest.com/2017/04/energy-threshold-calibration-in-speech-recognition.html
#
# Check if variable is string or int
# https://www.geeksforgeeks.org/python-check-if-a-variable-is-string/
#
# Kill thread/set as daemon thread
# https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
#
# https://www.youtube.com/watch?v=af9BF0Nu9ZQ
# https://www.youtube.com/watch?v=9GJ6XeB-vMg&t=70s
# https://www.youtube.com/watch?v=SXsyLdKkKX0
# https://www.youtube.com/watch?v=DiVMruyDm-U

# To open a application using python
# subprocess.call
# https://stackoverflow.com/questions/14831716/can-i-open-an-application-from-a-script-during-runtime

# listen background
# https://www.youtube.com/watch?v=p2vx-JliElY
# To install pyAudio, first install pipwin then pipwin install pyaudio

# Playback sounds
# https://stackoverflow.com/questions/20021457/playing-mp3-song-on-python
