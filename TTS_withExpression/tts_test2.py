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

import os, re
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.generic_utils import get_user_data_dir
from TTS.utils.manage import ModelManager

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

print(textt)
prompt = textt
# prompt = re.sub("([^\x00-\x7F]|\w)(\.|\。|\?)",r"\1 \2\2",textt)
print("Inference...")
out = model.inference(
    # "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
    prompt,
    "en",
    gpt_cond_latent,
    speaker_embedding,
    temperature=0.8, # Add custom parameters here
)

torchaudio.save("output.wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)
input("Press enter to exit ... ")

# THIS DRAMATICALLY SPED TTS PROCESS... BUT YOU NEED TO SACRIFISE THE QUALITY ... 
# QUALITY IS NOT BAD... IT IS DECENT 
# AND FOR LONG TEXTS, IT CUTS AFTER 1024 TOKENS
# ONE OPTION IS TO SPLIT THE TEXTS (NOT GOOD CHOICE)