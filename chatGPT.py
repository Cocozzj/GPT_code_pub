from utils.path_utils import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from seleniumbase import SB

ACCOUNT=['rjmpwfhgnr41@outlook.com',
           'berthiaumeFrederick759@hotmail.com']

LOGIN_URL = 'https://chat.openai.com/auth/login'
GPT4_URL = 'https://chat.openai.com/chat'

class Keys:
    """Set of special keys codes."""
    ENTER = "\ue007"
    CONTROL = "\ue009"
    SHIFT = "\ue008"


def wait_page_element(xpath,sb,flag=False):
    start_time = time.time()
    while (sb.is_element_visible(xpath) == flag and time.time() - start_time < 180):
        sb.sleep(0.1)

    return sb.is_element_visible(xpath) != flag

def login(sb):
    sb.open(GPT4_URL)
    print("!!!!")
    wait_page_element('//*[@id="__next"]/div[1]/div[2]/div[1]/div/div/button[1]', sb)
    sb.click('//*[@id="__next"]/div[1]/div[2]/div[1]/div/div/button[1]')

    try:
        sb.get_element('//*[@id="username"]',timeout=10)
    except:
        try:
            sb.click('//span[@class="ctp-label"]')
            sb.get_element('//*[@id="username"]', timeout=5)
        except:
            login(sb)
            return

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)

with SB(uc=True) as sb:
    login(sb)


