# TAKEN FROM : "https://huggingface.co/spaces/coqui/xtts/blob/main/app.py", 
#              "https://docs.coqui.ai/en/latest/models/xtts.html#id3"

# import time
# import torch
# import torchaudio
# import sys
# import io, os, stat
# import subprocess

# from TTS.api import TTS
# from TTS.tts.configs.xtts_config import XttsConfig
# from TTS.tts.models.xtts import Xtts
# from TTS.utils.generic_utils import get_user_data_dir
# from TTS.utils.manage import ModelManager

# repo_id = "coqui/xtts"

# print("Downloading if not downloaded Coqui XTTS V2")

# model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
# ModelManager().download_model(model_name)
# model_path = os.path.join(get_user_data_dir("tts"), model_name.replace("/", "--"))
# print("XTTS downloaded")

# config = XttsConfig()
# config.load_json(os.path.join(model_path, "config.json"))

import os, re, shutil
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.generic_utils import get_user_data_dir
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

from pydub import AudioSegment

def make_temp_dir(folder_path = "./", folder_name = "__temp_audio__"):
    _pathh = folder_path+folder_name
    if not os.path.exists(_pathh):
        os.mkdir(_pathh)
        print(f"{_pathh} created ...")
        return True 
    print(f"{_pathh} already exists...")
    return
    
def delete_temp(folder_path = "./__temp_audio__"):
    if os.path.exists(folder_path):
        # os.rmdir(folder_path)
        shutil.rmtree(folder_path)
        print(f"{folder_path} removed...")

print("Initializing synthesizer...")
syn = Synthesizer()
# ffmpeg_path = '../__temp__/ffmpeg/bin/ffmpeg.exe'
# assert os.path.exists(ffmpeg_path)

# AudioSegment.converter = ffmpeg_path

model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

model_path = os.path.join(get_user_data_dir("tts"), model_name.replace("/", "--"))
# print("XTTS downloaded")

repo_id = "coqui/xtts"

print("Downloading if not downloaded Coqui XTTS V2")
ModelManager().download_model(model_name)
model_path = os.path.join(get_user_data_dir("tts"), model_name.replace("/", "--"))
print("XTTS downloaded")

print("Loading model...")
config = XttsConfig()
config.load_json(os.path.join(model_path, "config.json"))

model_path = os.path.join(get_user_data_dir("tts"), model_name.replace("/", "--"))

model = Xtts.init_from_config(config)
model.load_checkpoint(
    config,
    checkpoint_path=os.path.join(model_path, "model.pth"),
    vocab_path=os.path.join(model_path, "vocab.json"),
    # eval=True,
    use_deepspeed=True,
    speaker_file_path=os.path.join(model_path, "speakers_xtts.pth") # THIS WAS GIVING ERROR
)
model.cuda()

ref_audio = "../__temp__/NEW Sage Voice Lines with other Agents  VALORANT.mp3"


print("Computing speaker latents...")
# gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["reference.wav"])
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[ref_audio])


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

textt = """Oho~ Testing out voice commands, are we? Sounds like fun, Brim. Let's give it a whirl and see if everything's running smoothly. What's the first command you want to try out?"""


# textt = "It took me quite a long time to develop a voice and now that I have it I am not going to be silent."

texts = syn.split_into_sentences(textt)
# input()

# print(textt)
print(texts)

# prompt = textt
# # prompt = re.sub("([^\x00-\x7F]|\w)(\.|\。|\?)",r"\1 \2\2",textt)
# print("Inference...")
# out = model.inference(
#     # "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
#     prompt,
#     "en",
#     gpt_cond_latent,
#     speaker_embedding,
#     temperature=0.8, # Add custom parameters here
# )

# torchaudio.save("output.wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)

temp_folder = "./__temp_audio__/"
temp_audio_files = []
combined_out = None
make_temp_dir()
for num, _text in enumerate(texts):
    prompt = _text+".."
    # prompt = re.sub("([^\x00-\x7F]|\w)(\.|\。|\?)",r"\1 \2\2", prompt)
    # prompt = re.sub("([^\x00-\x7F]|\w)(\.|\。|\?)",r"\1 \2\2",textt)
    print(f"{num} Inference...")
    out = model.inference(
        prompt,
        "en",
        gpt_cond_latent,
        speaker_embedding,
        temperature=0.7, # Add custom parameters here
    )
    _temp_audio_file = f"temp_out_{num}.wav"
    _temp_audio_filepath = temp_folder+_temp_audio_file

    temp_audio_files.append(_temp_audio_filepath)
    torchaudio.save(_temp_audio_filepath, torch.tensor(out["wav"]).unsqueeze(0), 24000)
    # assert os.path.exists(_temp_audio_file)
    # combined_out += AudioSegment.from_wav(_temp_audio_file)
assert all(map(os.path.exists, temp_audio_files))
# combined_out.export("output.wav", format="wav")
wavs = list(map(AudioSegment.from_wav, temp_audio_files))
combined = wavs[0]

for wav in wavs[1:]:
    combined = combined.append(wav)

delete_temp()
combined.export("output.wav", format="wav")

input("Press enter to exit ... ")

# THIS DRAMATICALLY SPED TTS PROCESS... BUT YOU NEED TO SACRIFISE THE QUALITY ... 
# QUALITY IS NOT BAD... IT IS DECENT 
# AND FOR LONG TEXTS, IT CUTS AFTER 1024 TOKENS
# ONE OPTION IS TO SPLIT THE TEXTS (NOT GOOD CHOICE)
# ADDED AN OPTION TO SPLIT LONGER TEXTS... QUALITY IS DECENT... PAUSE AND RELATION BETWEEN SENTENCES IS MISSING