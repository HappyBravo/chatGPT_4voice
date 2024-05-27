import time
from RealtimeSTT import AudioToTextRecorder
import logging
from dotenv import dotenv_values

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from getpass import getpass

from TTS_withExpression.tts import TTS_withExpression
import warnings

WAITER = 5
INPUT_WAITER = 3
countt = 0
options = uc.ChromeOptions()
# options.add_argument("--window-size=800,600")
# options.add_argument("--no-sandbox")
# options.add_argument('--headless') # HEADLESS IS NOT WORKING... 🫤
# options.add_argument("--headless=new")
# driver = uc.Chrome() #headless=True,use_subprocess=False)
# driver = webdriver.Chrome()

# Settings the warnings to be ignored 
warnings.filterwarnings('ignore')

def check_login_required(_driver):
    """
    Checks if the page requires login based on presence of "log in" or "sign up" text.

    Args:
        url: The URL of the webpage to check.
    """
    print("Checking text...")
    # # Open a browser instance
    # driver = webdriver.Chrome()  # Replace with your desired webdriver (e.g., Firefox)
    # driver.get(url)

    # Lowercase all text content for case-insensitive search
    page_text = _driver.page_source.lower()

    # Check for presence of "log in" or "sign up" text
    if "log in" in page_text or "sign up" in page_text:
        print("You need to login first")
        return 1
    return 0

def do_login(driver, user_email, user_password = ""):
    time.sleep(5)
    # wait = WebDriverWait(driver, 10)
    try :
        login_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[2]')
    except NoSuchElementException:
        print("Trying another method to search Login button")
        login_button = driver.find_element(By.CSS_SELECTOR('[data-testid="login-button"]'))
   
    # Click the button
    login_button.click()
    time.sleep(2)

    # Find the email input field
    # wait.until(EC.invisibility_of_element_located(((By.CLASS_NAME, "email-input"))))
    email_input = driver.find_element(By.CLASS_NAME, "email-input")

    # Enter your email address and press ENTER
    email_input.send_keys(user_email, Keys.ENTER)

    time.sleep(2)

    # Find the input using ID
    # wait.until(EC.invisibility_of_element_located((By.ID, "password")))
    password_input = driver.find_element(By.ID, "password")

    # Enter your desired keys
    if user_password:
        password_input.send_keys(user_password, Keys.ENTER)
        time.sleep(5)
    else:
        user_password = getpass()
        password_input.send_keys(user_password, Keys.ENTER)
        time.sleep(5)
    return driver 
        
def is_logged_in(driver):
    """
    Checks if "Sign up" and "Log in" buttons are not present, suggesting logged in state.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        True if buttons are not found, False otherwise (might not be logged in).
    """
    signUp_button = None
    logIn_button = None
    continueButton = None

    try:
        # Define waiting time (adjust as needed)
        # wait = WebDriverWait(driver, 10)
        
        # Try finding Sign Up button with a timeout
        # wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[text()='Sign Up']")))
        # wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[1]/div')))
        try :
            signUp_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[1]/div')
            print("Found Sign up button.")

        except NoSuchElementException:
            print("Sign up button not present")
            signUp_button = False
        # Try finding Log In button with a timeout
        # wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[text()='Log in']")))
        # wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[2]/div')))
        try:
            logIn_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[2]/div')
            print("Found Log In button.")
        
        except NoSuchElementException:
            print("Log In button not present")
            logIn_button = False
        try:
            continueButton = driver.find_element(By.XPATH, '/html/body/div[1]/main/section/div/div/div/form/div[2]/button')
            print("Found Continue button.")
        except:
            print("Continue button not present")
            continueButton = False
        # If no exceptions occur, likely logged in
        # return True
        if signUp_button or logIn_button or continueButton:
            return False
        else:
            print("No buttons found -> login successful !")
            time.sleep(0.5)
            return True
    # except NoSuchElementException:
    #     # One or both buttons might be present, indicating not logged in
    #     return False
    except Exception as e:
        # Handle other unexpected exceptions
        # print(f"Unexpected error: {e}")
        # return False
        print(f"Error: {e}")
        if any([logIn_button, signUp_button, continueButton]):
            return False
        
        print("No buttons found -> login successful !")
        time.sleep(5)
        return True

def send_text(driver, text):
    # Find the text area using ID
    text_area = driver.find_element(By.ID, "prompt-textarea")

    # Enter your desired text
    text_area.send_keys(text, Keys.ENTER)
    print(f"{'- - '*15} \n{text} \nSENT !")
    time.sleep(5)   # DEPENFING ON THE INTERNET SPEED
                    # KEEP THIS LONG IF YOU DO LONG CONVERSATIONS 


def extract_assistant_texts(driver):
    """
    Extracts text from conversation turns authored by the assistant.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        A list of strings containing the extracted assistant texts.
    """
    assistant_texts = []
    try:
        # ----------- SELENIUM BROWSER NEEDS TO BE IN FOCUS -------------
        # ----------- BECAUSE OF THIS, THESE WERE NOT WORKING -----------
        # ----------- COMMENTED OUT -------------------------------------
        # THE LOGIC WAS -
        #     IF THERE IS ACTIVE ELEMET ::after AFTER THE LAST PARAGRAPH,
        #     OR THE SEND BUTTON IS ACTIVE
        #     MEANIG CHATGPT IS WRITING SOME OUTPUT,
        #     WE SHOULD WAITER
        #     BUT THIS IS NOT WORKING IF I MINIMISE THE WINDOW 
        #
        # AND IF THE BROWSER WINDOW IS FOCUSED, 
        #     THERE IS NO NEED TO LOOK FOR THE ACTIVE ELEMENT AS time.sleep() DOES THE JOB
        # ----------------------------------------------------------------
        # ----------------------------------------------------------------
        # ----------------------------------------------------------------

        # driver.implicitly_wait(5)

        # Wait until the button is present and becomes disabled
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[1]/div[2]/main/div[1]/div[2]/div[1]/div/form/div/div[2]/div/div/button[@data-testid='fruitjuice-send-button'][@disabled]"))
        # )

        # element_locator = (By.CSS_SELECTOR, "div[data-message-author-role='assistant'] div.markdown.prose")

        # Wait until the last element is present
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))

        # # # Now, wait until the last element stops updating (indicating animation is complete)
        # last_element = driver.find_elements(*element_locator)[-1]
        # WebDriverWait(driver, 10).until(
        #     lambda driver: last_element == driver.find_elements(*element_locator)[-1]
        # )
        # # Wait until the :after pseudo-element disappears
        # WebDriverWait(driver, 10).until(
        #     lambda driver: not last_element.find_elements(By.CSS_SELECTOR, "::after")
        # )
        # # Wait until the :after pseudo-element disappears
        # WebDriverWait(driver, 10).until(EC.staleness_of(assistant_messages[-1]))

        # # Wait until the button is present and not disabled
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fruitjuice-send-button'][disabled])")))

        time.sleep(2)
      
        # Find elements with data-message-author-role='assistant'
        assistant_messages = driver.find_elements(By.CSS_SELECTOR, "div[data-message-author-role='assistant'] div.markdown.prose")
        # Extract and print the text from these elements
        for message in assistant_messages:
            # print(message.text)
            assistant_texts.append(message.text)

    except Exception as e:
        print(f"Error extracting assistant texts: {e}")
    
    return assistant_texts

chatgpt_url = "https://chatgpt.com/"

config = dotenv_values(".env")
# print(config)

if __name__ == "__main__":
    driver = uc.Chrome(options=options)
    driver.set_window_size(800, 600)
    # driver.minimize_window()

    driver.get(chatgpt_url)
    # driver.implicitly_wait(5)

    time.sleep(5)
    
    logged_in = False

    def recording_started():
        print("Speak now...")

    def recording_finished():
        print("Speech end detected... transcribing...")

    recorder_config = {
        'spinner': False,
        # 'model': 'large-v2',
        'model':"base",
        'language': 'en',
        'silero_sensitivity': 0.4,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 0.3,
        'min_length_of_recording': 0.3,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.2,
        # 'realtime_model_type': 'tiny.en',
        'realtime_model_type': 'base.en',

        # 'on_realtime_transcription_update': text_detected, 
        # 'on_realtime_transcription_stabilized': text_detected,
        # 'level' : logging.DEBUG,
        # 'wake_words':"hey google",
        # 'on_wakeword_detected' : recording_started, 
        # 'on_recording_stop' : recording_finished
    }

    def STT():
        # # # # # # # # # # # # #
        # THIS NEEDS TO BE INSIDE __name__ == "__main__"
        # # # # # # # # # # # # # 
        _decide = ""

        with AudioToTextRecorder(**recorder_config) as recorder:
            # print('Say "Jarvis" then speak.')
            init_text = ""
            stt_output = ""
            _countt = 0
            full_sentences = []
            empty_user_input_countt = 0
            empty_user_input_limit = 3
            while True:
                _wait = 0
                user_text = ""
                if empty_user_input_countt >= empty_user_input_limit :
                    print(f"Empty user_inputs for more than {empty_user_input_limit} times...")
                    
                    _decide = ""
                    for _ in range(3):
                        _decide = input("Press 1 or ENTER to continue, 0 to stop : ").strip()
                        if _decide not in ["", '1', '0']:
                            continue
                        break
                    else:
                        # recorder.stop()
                        print("Exiting STT...")
                        break

                    if _decide == '0':
                        break
                    empty_user_input_countt = 0
                    full_sentences = []
                    _countt = 0
                    continue
            
                init_text = " ".join(full_sentences)
                # user_text = recorder.text()
                recorder.start()
                
                _wait = WAITER*(not bool(_countt)) + INPUT_WAITER*bool(_countt) 
                print(f"Waiting {_wait} sec...")
                time.sleep(_wait)
                
                user_text = recorder.text()
                # print(user_text)
                if len(set(user_text.strip().split())) > 1 or \
                                        user_text.strip().lower() not in ["", "you.", "you .", "you"]: # 0: 
                                                            # there are some ghoset inputs of "You. You. You." 
                                                            # - maybe due to fan or some noise 🤔
                    full_sentences.append(user_text)
                    _countt += 1
                    continue
                else :
                    empty_user_input_countt += 1

                if len(" ".join(full_sentences)) == len(init_text) and _countt > 0:
                    break

            print("Stopping STT...")
            # print("Done. Now we should exit.")
            recorder.stop()
            stt_output = " ".join(full_sentences)
            if stt_output.strip():
                print("You said - ")
                print(" ".join(full_sentences), end = "\n")
            if _decide == "0":
                stt_output = "<< EXIT >>"
        return stt_output

    if check_login_required(driver):
        try_login_countt = 0
        print("Trying to log in")
        time.sleep(2)
        driver = do_login(driver, user_email=config['USER_EMAIL'], user_password=config["USER_PASSWORD"])
        while try_login_countt < 3:
            if is_logged_in(driver):
                logged_in = True
                print("Login successful !")
                time.sleep(2)
                break
            else:
                print("Maybe check the credentials and try to login manually ?")
                input("PRESS ENTER WHEN DONE MANUAL LOGIN ... ")
            try_login_countt += 1
            
    ref_audio = "./__temp__/NEW Sage Voice Lines with other Agents  VALORANT.mp3"
    out_audio_file = "output.wav"

    if logged_in:
        # driver.minimize_window()  # <-- CAN'T DO THIS 🫥
                                    #     SELENIUM GOES OUT OF FOCUS 
                                    #     SO ELEMENTS ARE NOT VISIBLE TO THE CODE. 

        print("Initializing TTS...")
        tts_engine = TTS_withExpression()

        print("Initializing STT and trying to do the inputs ... ")
        time.sleep(2)
        user_input = ""
        countt = 0
        empty_user_input_countt = 0
        empty_user_input_limit = 2
        while True:
            
            user_input = STT()
            countt += 1
            
            if not user_input:
                empty_user_input_countt += 1
                continue
            if user_input == "<< EXIT >>":
                break
            
            send_text(driver, user_input)
            empty_user_input_countt = 0
            time.sleep(3)
            gpt_responses = extract_assistant_texts(driver)
            # print(gpt_responses)
            if gpt_responses:
                print("ChatGPT [002] -")
                response = gpt_responses[-1]
                print(gpt_responses[-1], end="\n")

                # # # # # # # # # # # # # 
                # NEED TO MAKE A FUNCTION FOR PRE-PROCESSING
                # -- CODE BLOCKS CAN BE EXCLUDED IN PRE-PREPROCESSING
                # -- WORDS WHICH IS NON-ENGLISH OR WORDS WHICH ARE NOT OF YOUR TTS's MODEL LANGUAGE SHOULD BE CHANGED
                # 
                response = response.replace("ダーリン", "dah-ring") # PREPROCESSION BEFORE TTS 
                # # # # # # # # # # # #

                tts_engine.cook_voice(text=response, 
                                      ref_audio_path=ref_audio)
                tts_engine.play_voice(audio_path=out_audio_file)
                empty_user_input_countt = 0

            user_input = ""
            time.sleep(0.5)
    else:
        print("Login unsuccessful. Try again after sometime ...")

    driver.close()

    time.sleep(2)
    print(f"Loop ran for {countt} times...")
    input("Enter to EXIT...")
