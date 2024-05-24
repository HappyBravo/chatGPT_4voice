import time
from RealtimeSTT import AudioToTextRecorder
import logging
from dotenv import dotenv_values

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException

from getpass import getpass

WAITER = 5
INPUT_WAITER = 3
countt = 0
options = uc.ChromeOptions()
# options.add_argument("--window-size=800,600")
# options.add_argument("--no-sandbox")
# driver = uc.Chrome() #headless=True,use_subprocess=False)
# driver = webdriver.Chrome()

# def checkLogin():
#     # Let's find the text
#     if driver.find_elements(By.XPATH, "//*[contains(text(), 'log in')]"):
#         print("Found it")
#     else:
#         print("Sorry, couldn't find it.")

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
    # pass
    # Find the button using XPath
    # login_button = driver.find_element(By.XPATH, "//button[text()='Log in']")
    login_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[2]')

    # login_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="tesging button"]')

    # Click the button
    login_button.click()
    time.sleep(2)

    # Find the email input field
    email_input = driver.find_element(By.CLASS_NAME, "email-input")

    # Enter your email address and press ENTER
    # email_input.send_keys("your_email_id@example.com")
    email_input.send_keys(user_email, Keys.ENTER)

    time.sleep(2)

    # Find the input using ID
    password_input = driver.find_element(By.ID, "password")

    # Enter your desired keys
    if user_password:
        password_input.send_keys(user_password, Keys.ENTER)
        time.sleep(10)
    else:
        user_password = getpass()
        password_input.send_keys(user_password, Keys.ENTER)
        time.sleep(10)
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

    try:
        # Define waiting time (adjust as needed)
        # wait = WebDriverWait(driver, 10)
        
        # Try finding Sign Up button with a timeout
        # wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[text()='Sign Up']")))
        # wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[1]/div')))
        signUp_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[1]/div')
        # Try finding Log In button with a timeout
        # wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[text()='Log in']")))
        # wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[2]/div')))
        logIn_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[2]/div')
        
        # If no exceptions occur, likely logged in
        # return True
        if signUp_button and logIn_button:
            return False
    # except NoSuchElementException:
    #     # One or both buttons might be present, indicating not logged in
    #     return False
    except Exception as e:
        # Handle other unexpected exceptions
        print(f"Error: {e}")
        if any([logIn_button, signUp_button]):
            return False
        
        print("No buttons found -> login successful !")
        time.sleep(5)
        return True

def send_text(driver, text):
    # Find the text area using ID
    text_area = driver.find_element(By.ID, "prompt-textarea")

    # Enter your desired text
    text_area.send_keys(text, Keys.ENTER)
    print(f"{'- - '*10} \n{text} \n SENT !")
    time.sleep(10)

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
        # Wait for conversation elements to load (adjust timeout as needed)
        # wait = WebDriverWait(driver, 10)
        time.sleep(10)
        # conversation_turns = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "group/conversation-turn")))
        conversation_turns = driver.find_elements(By.CLASS_NAME, "group/conversation-turn")
        for turn in conversation_turns[-10:]: # LAST FEW ONLY NEEDED
            # Check for inner div with assistant role
            if turn.find_element(By.XPATH, ".//div[@data-message-author-role='assistant']"):
                # Extract text from the conversation turn
                text = turn.text.strip()
                assistant_texts.append(text)
    except Exception as e:
        print(f"Error extracting assistant texts: {e}")
    
    return assistant_texts

chatgpt_url = "https://chatgpt.com/"

config = dotenv_values(".env")
# print(config)

if __name__ == "__main__":
    driver = uc.Chrome(options=options)
    driver.get(chatgpt_url)

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
        'post_speech_silence_duration': 0.4,
        'min_length_of_recording': 0.5,
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
        stt_output = ""
        countt = 0
        with AudioToTextRecorder(**recorder_config) as recorder:
            # print('Say "Jarvis" then speak.')
            init_text = ""
            full_sentences = []
            while True:
                init_text = " ".join(full_sentences)
                # user_text = recorder.text()
                recorder.start()

                if countt == 0:
                    print(f"Waiting {WAITER} sec...")
                    time.sleep(WAITER)
                else:
                    print(f"Waiting {INPUT_WAITER} sec...")
                    time.sleep(INPUT_WAITER)
                
                user_text = recorder.text()

                if len(user_text) > 0:
                    full_sentences.append(user_text)

                if len(" ".join(full_sentences)) != len(init_text):
                    countt += 1
                    continue
                else:
                    recorder.stop()
                    break

            print("Done. Now we should exit.")
            stt_output = " ".join(full_sentences)
            print("You said - ")
            print(" ".join(full_sentences))
        return stt_output

    time.sleep(5)

    if check_login_required(driver):
        print("Trying to log in")
        time.sleep(2)
        driver = do_login(driver, user_email=config['USER_EMAIL'])
        if is_logged_in(driver):
            logged_in = True
            print("Login successful !")
            time.sleep(2)

    if logged_in:
        print("Initializing STT and trying to do the inputs ... ")
        time.sleep(2)
        user_input = ""
        countt = 0
        while True:
            user_input = STT()
            countt+=1
            if not user_input:
                continue
            send_text(driver, user_input)
            time.sleep(5)
            gpt_responses = extract_assistant_texts(driver)
            print(gpt_responses[-1])
            user_input = ""
            time.sleep(0.5)

    driver.close()

    time.sleep(4)
    print(f"Loop ran for {countt} times...")
    input("Enter to EXIT...")