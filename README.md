# USE CHATGPT WITH VOICE INPUT AND OUTPUT ON YOUR LAPOT

With the introduction of ChatGPT-4o, I found that you can add some customisations to how ChatGPT response your question.

I decided to giver her a personality. Similar to [character.ai](character.ai) 🌚. 
Also, I thought of making it as a Assistant Chatbot like Google Assistant on Androif phones.

*But as I went on building this project, I found that that cannot be done. Due to the limitations of libraries used in the project.* 🫤

---
---
### THE GENERAL SCHEME IS AS FOLLOWS -
- STT - for voice input
- [chatgpt.com](chatgpt.com) - for making response (coz LLM on lapot takes too much time to respond. and is not as good as ChatGPT.)
- TTS (with expressions) - for audio response

---
---

### HARDWARE REQUIREMENTS (! IMPORTANT 😬 !) 
- NVIDIA GPU WITH 4 GB OR MORE VRAM
    - IF VRAM IS LESS, YOU CAN TRY SMALLER STT MODELS WHICH ARE ABOUT 300 - 500 MB 
    - OR IF NO GPU, YOU CAN TRY [pyttsx3](https://pyttsx3.readthedocs.io/en/latest/index.html) (but it kills the purpose 🫥) <<--- *THIS PART IS NOT CODE YET 😬*
- ATLEAST 10 GB SSD SPACE. (HDD WILL BE SLOW)
    - STT MODELS ARE AROUND 2 GB AND TORCH+CUDA AND OTHER STUFFS WILL TAKE ABOUT 6-7 GB. 
- 16 GB OR MORE RAM (I HAVE NOT CHECKED THE PERFORMANCE ON 8 GB RAM)

--- 
### SETUP
- MAKE A .env FILE WITH
  ```
  USER_EMAIL : your_email@eamil.com
  USER_PASSWORD : your_password
  ```
  - OR YOU CAN MANUALLY PUT YOUR EMAIL IN THE CODE (not recommended) \
  - PASSWORD CAN BE KEPT EMPTY, DURING THE RUNTIME, THE PROGRAM WILL ASK FOR PASSWORD IN THAT CASE

---
---

### will populate this later ... 😴