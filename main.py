import random
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import os
import time
URL = ""
DRIVER_WAIT = 10
USER_WAIT = 30

data = open('config.txt', 'r').readlines()

CONFIG = {}

for line in data:
    key, value = (x.strip() for x in line.split('='))
    CONFIG[key] = value

PROFILE_DIR = CONFIG['user_dir']
PROFILE = CONFIG['profile']
COMMENTS_FILE = CONFIG['comments_file']
COOLDOWN_TIME = CONFIG['cooldown_time']

# livestream_code = "ww4tDA3SekA"
livestream_code = ""

def send_comment(driver, comment):
    wait = WebDriverWait(driver, 10)
    comment_input_parent = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'yt-live-chat-text-input-field-renderer#input')))
    comment_input = comment_input_parent.find_element(By.CSS_SELECTOR, 'div#input')
    driver.execute_script('arguments[0].textContent = arguments[1];', comment_input, comment)
    driver.execute_script('arguments[0].dispatchEvent(new Event("input"));', comment_input)
    send_button = driver.find_element(By.CSS_SELECTOR, 'button#button[aria-label=Send]')
    send_button.click()

def load_comments(comments_file):
    for l in open(comments_file, 'r', encoding='utf-8').readlines():
        yield l.strip()

def setup(profile_dir, profile, comments_file, cooldown_time):
    options = Options()
    options.add_argument("--disable-notifications")
    
    options.add_argument(f"--user-data-dir={os.path.abspath(profile_dir)}")
    options.add_argument(f"--profile-directory={profile}")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("useAutomationExtension", False)

    services = Service(executable_path=ChromeDriverManager().install())
    driver = Chrome(service=services, options = options)
    
    driver.get(f"https://www.youtube.com/live_chat?is_popuot=1&v={livestream_code}")
    
    comments = load_comments(comments_file)
    for c in comments:
        send_comment(driver, c)
        time.sleep(float(cooldown_time))
    print("All comments done.")
    input("[?] Want to close (y/n): ")

if __name__ == '__main__':
    input("Note: You have to close all chrome profile to run script. [!] Press enter to close all profile: ")
    os.system('taskkill /f /im chrome.exe')
    try:
        livestream_code = input("Enter livestream video id: ")
        if(livestream_code):
            setup(PROFILE_DIR, PROFILE, COMMENTS_FILE, COOLDOWN_TIME)
        else: 
            print("Livestream video id not provided. Try again..")
            exit()
    except Exception as e:
        print('[!] Chrome already opened! Kindly close all open chrome browser instances and then run the program.')
        print(e)