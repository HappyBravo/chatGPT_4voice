# USE CHATGPT WITH VOICE INPUT AND OUTPUT ON YOUR LAPOT

With the introduction of ChatGPT-4o, I found that you can add some customisations to how ChatGPT response your question.

I decided to giver her a personality (002 in my case). Similar to [character.ai](character.ai) 🌚. 

Also, I thought of making it as a Assistant Chatbot like Google Assistant on Android phones. *But as I went on building this project, I found that that cannot be done. Due to the limitations of libraries used in the project.* 🫤

[DEMO](https://www.youtube.com/watch?v=-lx_MS_-YeE)
---
---
### 🤔 THE GENERAL SCHEME IS AS FOLLOWS -
- STT - for voice input
- [chatgpt.com](chatgpt.com) - for making response (coz LLM on lapot takes too much time to respond. and is not as good as ChatGPT) (* USE IT ON YOUR OWN RISK *)
- TTS (with expressions) - for audio response

---
---

### 🖥️ HARDWARE REQUIREMENTS ( IMPORTANT 😬 ) 
- NVIDIA GPU WITH 4 GB OR MORE VRAM
    - IF VRAM IS LESS, YOU CAN TRY SMALLER STT MODELS WHICH ARE ABOUT 300 - 500 MB 
    - OR IF NO GPU, YOU CAN TRY [pyttsx3](https://pyttsx3.readthedocs.io/en/latest/index.html) (but it kills the purpose 🫥) <<--- *THIS PART IS NOT CODED YET 😬*
- ATLEAST 10 GB SSD SPACE. (HDD WILL BE SLOW)
    - [STT MODELS](https://huggingface.co/coqui/XTTS-v2/tree/main) ARE AROUND 2 GB AND [TORCH+CUDA](https://pytorch.org/) AND OTHER STUFFS WILL TAKE ABOUT 6-7 GB. 
- 16 GB OR MORE RAM (I HAVE NOT CHECKED THE PERFORMANCE ON 8 GB RAM)

--- 
### 🔧 SETUP
- MAKING A NEW ENVIRONMENT WILL BE BETTER
  - LOOK [HERE](https://www.geeksforgeeks.org/python-virtual-environment/) TO KNOW MORE AND FOR INSTRUCTIONS 
- MAKE A `.env` FILE IN THE ROOT FOLDER OF THE PROJECT WITH THESE ENTITIES -
  ```
  USER_EMAIL : your_email@eamil.com
  USER_PASSWORD : your_password
  ```
  - OR YOU CAN MANUALLY PUT YOUR EMAIL IN THE CODE (not recommended)
  - PASSWORD CAN BE KEPT EMPTY, DURING THE RUNTIME, THE PROGRAM WILL ASK FOR PASSWORD IN THAT CASE

---
---

### 📎 REQUIREMENTS 
INSTALL THESE PACKAGES -
- dotenv
- [undetected_chromedriver](https://pypi.org/project/undetected-chromedriver/)
- selenium
- getpass
- [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT)
- [torch + cuda](https://pytorch.org/)
- pygame 
- pynput
- [TTS](https://docs.coqui.ai/en/latest/installation.html)
- ChatGPT account

RealtimeSTT may not work correctly with recent version of torch+CUDA, just google about it, you should get some solution.\
Make sure that Torch + CUDA is setup correctly - check [this](https://stackoverflow.com/questions/48152674/how-do-i-check-if-pytorch-is-using-the-gpu) \
Now at the end, you will need a reference "high quality" voice that you want your AI Assistant to emulate. *(Find your Waifu/Husbando 😉)*

---
---

### will populate this later ... 😴