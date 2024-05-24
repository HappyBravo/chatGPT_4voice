# import speech_recognition as sr

# # Initialize the recognizer
# recognizer = sr.Recognizer()

# recognizer.recognize_whisper(audio_file)


# # Load an audio file
# audio_file = "./__temp__/sample_audio.wav"

# # Open the audio file
# with sr.AudioFile(audio_file) as source:
#     # Record the audio data
#     audio_data = recognizer.record(source)

#     try:
#         # Recognize the speech
#         text = recognizer.recognize_google(audio_data)
#         print("Recognized speech: ", text)
#     except sr.UnknownValueError:
#         print("Speech recognition could not understand the audio.")
#     except sr.RequestError as e:
#         print(f"Could not request results from service; {e}")

from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama
import os, time
import keyboard 

print("Initializing RealtimeSTT test...")

colorama.init()

full_sentences = []
displayed_text = ""

def clear_console():
    os.system('clear' if os.name == 'posix' else 'cls')

def text_detected(text):
    global displayed_text
    sentences_with_style = [
        f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
        for i, sentence in enumerate(full_sentences)
    ]
    new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

    if new_text != displayed_text:
        displayed_text = new_text
        clear_console()
        print(displayed_text, end="", flush=True)

recorder_config = {
        'spinner': False,
        # 'model': 'large-v2',
        'model':"base",
        'language': 'en',
        'silero_sensitivity': 0.4,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 0.4,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.2,
        # 'realtime_model_type': 'tiny.en',
        'realtime_model_type': 'base.en',

        'on_realtime_transcription_update': text_detected, 
        # 'on_realtime_transcription_stabilized': text_detected,
        
    }

recorder = AudioToTextRecorder(**recorder_config)

def process_text(text):
    full_sentences.append(text)
    text_detected("")

clear_console()

print("Say something...", end="", flush=True)

# while True:
    # recorder.text(process_text)

# recorder = AudioToTextRecorder()

# input("Press ENTER to start :")
# recorder.start()

# input("Press ENTER to stop :")
# recorder.stop()

# print(recorder.text())


if __name__ == '__main__':
    # recorder = AudioToTextRecorder(spinner=False, model="tiny.en", language="en")
    recorder = AudioToTextRecorder(**recorder_config)

    print("Say something...")
    while (True): print(recorder.text(), end=" ", flush=True)
    # history = []
    # while True:
    #     # Wait until user presses space bar
    #     print("\n\nTap space when you're ready. ", end="", flush=True)
    #     keyboard.wait('space')
    #     while keyboard.is_pressed('space'): pass

    #     # Record from microphone until user presses space bar again
    #     print("I'm all ears. Tap space when you're done.\n")
    #     recorder.start()
    #     while not keyboard.is_pressed('space'): 
    #         time.sleep(0.1)  
    #     user_text = recorder.stop().text()
    #     print(f'>>> {user_text}\n<<< ', end="", flush=True)
    #     history.append({'role': 'user', 'content': user_text})
