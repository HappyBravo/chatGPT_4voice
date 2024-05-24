# TAKEN FROM "https://github.com/KoljaB/RealtimeSTT/blob/master/tests/realtimestt_test.py"

from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama
import os, time

import time
import threading

def get_user_input_with_timeout(timeout1=5, timeout2=3):
    """
    Gets user input with a timeout mechanism.

    Args:
        timeout1 (int, optional): Initial timeout in seconds for user input (default: 5).
        timeout2 (int, optional): Subsequent timeout in seconds if user keeps entering input (default: 3).

    Returns:
        str: The user's input, or an empty string if no input is received within the timeouts.
    """

    user_input = ""
    stop_flag = threading.Event()  # Event to signal stopping input capture
    
    def process_text(text):
        full_sentences.append(text)
        text_detected("")
    full_sentences = []
    displayed_text = ""
    def capture_input():
        nonlocal user_input, stop_flag
        while not stop_flag.is_set():
            try:
                # recorder.start()
                while True:
                    recorder.text(process_text)
                # new_input = input()
                # user_input += new_input
            except EOFError:  # Handle end-of-file (Ctrl+D)
                break

    # Start a thread to capture user input concurrently
    input_thread = threading.Thread(target=capture_input)
    input_thread.start()

    # Wait for initial timeout
    time.sleep(timeout1)

    if user_input:  # User entered something, switch to shorter timeout
        while True:
            time.sleep(timeout2)
            if not stop_flag.is_set() and not input_thread.is_alive():
                # User stopped entering input or thread finished, break the loop
                break

    # Signal the thread to stop
    stop_flag.set()

    # Wait for the thread to join (ensure it finishes)
    input_thread.join()

    return user_input

# # Example usage
# user_input = get_user_input_with_timeout()
# if user_input:
#   print("You entered:", user_input)
# else:
#   print("No input received within the timeout.")


if __name__ == '__main__':

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

    # def text_detected(text):
    #     global displayed_text
    #     clear_console()
    #     print(text)
        # sentences_with_style = [
        #     f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
        #     for i, sentence in enumerate(full_sentences)
        # ]
        # new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

        # if new_text != displayed_text:
        #     displayed_text = new_text
        #     clear_console()
        #     print(displayed_text, end="", flush=True)

    def process_text(text):
        full_sentences.append(text)
        text_detected("")

    recorder_config = {
        'spinner': False,
        # 'model': 'large-v2',
        'model' : 'base',
        'language': 'en',
        'silero_sensitivity': 0.4,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 0.4,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.2,
        'realtime_model_type': 'tiny.en',
        'on_realtime_transcription_update': text_detected, 
        #'on_realtime_transcription_stabilized': text_detected,
    }

    recorder = AudioToTextRecorder(**recorder_config)

    clear_console()
    print("Say something...", end="", flush=True)

    while True:
        init_text = ""
        user_text = ""
        countt = 0
        recorder.start()
        # while countt == 0 and user_text == "":
        time.sleep(1)
        if (init_text == user_text) and user_text != "":
            # break
            # recorder.text(process_text)
            user_text = recorder.stop().text()
            init_text = user_text
        print(f'>>> {user_text}\n<<< ', end="", flush=True)
    print("Exitt")
    input("Enter to continue...")