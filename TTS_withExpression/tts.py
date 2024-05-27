import torch
from TTS.api import TTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pynput.keyboard import Key, Listener
import math, time
import threading

class TTS_withExpression():
    def __init__(self, 
                 TTS_model = "tts_models/multilingual/multi-dataset/xtts_v2",
                 useGPU = True):
        self.sound_length = 0
        self._sound = None
        self.device = "cpu"
        self.stop_event = None
        if useGPU:
            # self.device = self.get_device(useGPU)
            self.device = "cuda" if torch.cuda.is_available() else "cpu" 

        if not TTS_model:
            TTS_model = input("Enter TTS model to use : ").strip()
        
        print("Loading TTS model...")
        self.tts = TTS(TTS_model).to(self.device)
        print("TTS model loaded...")

        print("initializing pygame...")
        pygame.init()
        print("pygame initiated...")


    def get_device(self, useGPU=True):
        if useGPU:
            return "cuda" if torch.cuda.is_available() else "cpu"
    
    def cook_voice(self, text, 
                   ref_audio_path = None, 
                   lang = "en", 
                   output_file = "output.wav"):
        if not ref_audio_path:
            print("WARNING :: May give error depending on your model...")
        else:
            assert os.path.exists(ref_audio_path)
        
        self.tts.tts_to_file(text=text, 
                             speaker_wav=ref_audio_path, 
                             language=lang, 
                             file_path=output_file)
        print(f"Audio generated to '{output_file}'...")

    def checkPressSpace(self, key):
        if key == Key.space or not pygame.mixer.get_busy():
            print("stopping audio ...")
            if self._sound:
                self._sound.stop()
                self._sound = None
            else:
                pygame.mixer.stop()
            self.stop_event.set()
            # time.sleep(1)
            return False
        
    def monitor_audio_time(self):
        # while pygame.mixer.get_busy():
        while True:
            if time.time() - audio_start_time > 1 + self.sound_length:
                if self._sound:
                    self._sound.stop()
                    self._sound = None
                else:
                    pygame.mixer.stop()
                print("Audio stopped due to timeout.")
                self.stop_event.set()
                # time.sleep(1)
                return False
            # time.sleep(1)

    def listen_for_key_press(self):
        # Listen for space key press
        with Listener(on_press=self.checkPressSpace) as listener:
            listener.join()
        self.stop_event.set()

    def play_voice(self, audio_path = ""):
        global audio_start_time

        if os.path.exists(audio_path):
            self._sound = pygame.mixer.Sound(audio_path)
            
            self.sound_length = int(math.ceil(pygame.mixer.Sound.get_length(self._sound)))
            self._sound.play()
            audio_start_time = time.time()
            # flag = 0
            
            # - - - - - - - - - - - - - - - - - - - - - - - - - 
            # THE LOGIC IS -
            # -- MAKE TWO THREAD, 
            #     -- SEE IF USER PRESSES SPACE BUTTON ON KEYBOARD, STOP THE AUDIO RESPONSE
            #     -- OR IF THE AUDIO RESPONSE HAS BEEN PLAYED. THEN STOP THE OTHER THREAD 
            # -- FINALLY MAKE SURE THAT BOTH THREADS ARE STOPPED
            # - - - - - - - - - - - - - - - - - - - - - - - - - 

            # Initialize stop event
            self.stop_event = threading.Event()
            
            # Start a separate thread to monitor audio playback time
            monitor_thread = threading.Thread(target=self.monitor_audio_time)
            monitor_thread.start()

             # Start thread for listening for key presses
            key_listener_thread = threading.Thread(target=self.listen_for_key_press)
            key_listener_thread.start()

            # Check if any thread has finished
            while monitor_thread.is_alive() or key_listener_thread.is_alive():
                if not monitor_thread.is_alive() or not key_listener_thread.is_alive():
                    print("Stopping threads ...")
                    self.stop_event.set()
                    break
                # time.sleep(1)
        return

        


