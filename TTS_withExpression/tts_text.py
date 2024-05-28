####
# IT SHOULD BE ABLE TO PLAY THESE KINDS ON SENTENCES...
SAMPLE_TEXT = """Oh ? Testing out your voice input, huh, ダーリン? Well, how's it going so far ? Got any juicy gossip to spill about how it handles my voice ?"""
# "ダーリン" : "dah-ring"
###

import torch
from TTS.api import TTS
import os
import pygame
from pynput.keyboard import Key, Listener

pygame.init()

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
# print(TTS().list_models())
# input("enter to continue ... ")

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
# tts = TTS("tts_models/en/ljspeech/vits").to(device) # <-- GIVES SOME ERROR
# tts = TTS("tts_models/en/vctk/vits").to(device)


# Text to speech list of amplitude values as output
# ref_audio = "../__temp__/Voicy_Valorant Sage My purpose is my gift be not afraid t .wav"
ref_audio = "../__temp__/NEW Sage Voice Lines with other Agents  VALORANT.mp3"
assert os.path.exists(ref_audio)

# wav = tts.tts(text="Hello world!", speaker_wav=ref_audio, language="en")

# textt = SAMPLE_TEXT.replace("ダーリン", "dah-ring")
# textt = SAMPLE_TEXT.replace("ダーリン", "")
textt = """Oho~ Testing out voice commands, are we? Sounds like fun, Brim. Let's give it a whirl and see if everything's running smoothly. What's the first command you want to try out?"""

textt = """
Sure, I'll convert the text to English phonetics for you:

kaise ho dost?
All good?
watashi mo genki desu.
see you then..."""

textt = """Alright, ダーリン, let's start with some basics.

For greetings:
- "Hello" is "Konnichiwa" (こんにちは).
- "Good morning" is "Ohayou" (おはよう).
- "Good evening" is "Konbanwa" (こんばんは).

For simple pronouns:
- "I" is "Watashi" (私).
- "You" is "Anata" (あなた).

Some common words:
- "Yes" is "Hai" (はい).
- "No" is "Iie" (いいえ).
- "Thank you" is "Arigatou" (ありがとう).

How does that sound to start, ダーリン?"""

textt = """Sure thing! Here are some common phrases you might find useful:

1. "Konnichiwa" (こんにちは) - Hello
2. "Arigatou" (ありがとう) - Thank you
3. "Sumimasen" (すみません) - Excuse me/I'm sorry
4. "Hai" (はい) - Yes
5. "Iie" (いいえ) - No
6. "Ohayou gozaimasu" (おはようございます) - Good morning
7. "Konbanwa" (こんばんは) - Good evening
8. "Sayounara" (さようなら) - Goodbye
9. "O genki desu ka?" (おげんきですか) - How are you?
10. "Genki desu" (げんきです) - I'm fine

Feel free to ask if you need more translations or explanations, ダーリン."""

print(textt)
# Text to speech to a file
# tts.tts_to_file(text="Hello world!", speaker_wav=ref_audio, language="en", file_path="output.wav")
tts.tts_to_file(text=textt, speaker_wav=ref_audio, language="en", file_path="output.wav")
# tts.tts_to_file(text=textt, language="en", file_path="output.wav")


# PLAYING SOUND
my_sound = pygame.mixer.Sound('output.wav')
my_sound.play()

# paused = False
# running = True
# while running and not paused:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 paused = not paused
#                 if paused:
#                     pygame.mixer.music.stop()

def checkSpace(key):
    if key == Key.space:
        print("stopping audio ...")
        return False
 
while True:
    # Collect all event until released
    with Listener(on_press = checkSpace) as listener:
        listener.join()
    my_sound.stop()
    break

input("ENTER to exit...")