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
GPT4_URL = 'https://chat.openai.com/chat/'

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

class login_gpt():
    def __init__(self,username,pwd):
        self.username = username
        self.pwd = pwd
    def login(self,sb):
        sb.open(LOGIN_URL)
        wait_page_element('//*[@id="__next"]/div[1]/div[2]/div[1]/div/div/button[1]', sb)
        sb.click('//*[@id="__next"]/div[1]/div[2]/div[1]/div/div/button[1]')

        try:
            sb.get_element('//*[@id="username"]',timeout=5)
        except:
            try:
                sb.click('//span[@class="ctp-label"]')
                sb.get_element('//*[@id="username"]', timeout=3)
            except:
                self.login(sb)
                return
            
        wait_page_element('//*[@id="username"]', sb)
        sb.update_text('//*[@id="username"]', self.username)
        sb.click('/html/body/div/main/section/div/div/div/div[1]/div/form/div[2]/button')



def login(self,sb):
    

    # 防止人机验证
    try:
        sb.get_element('//*[@id="username"]',timeout=5)
    except:
        try:
            sb.click('//span[@class="ctp-label"]')
            sb.get_element('//*[@id="username"]', timeout=3)
        except:
            self.login(sb)
            return

    # 等待进入信息输入页面后输入用户名并点击continue
    wait_page_element('//*[@id="username"]', sb)
    sb.update_text('//*[@id="username"]', self.username)
    sb.click('/html/body/div/main/section/div/div/div/div[1]/div/form/div[2]/button')

    # 等待进入输入密码页面
    wait_page_element('//*[@id="password"]', sb)
    # 输入密码，点击登录
    sb.click('//*[@id="password"]')
    sb.send_keys('//*[@id="password"]', self.pwd)
    sb.send_keys('//*[@id="password"]', Keys.ENTER)
    sb.sleep(1)
    # 预防没有成功回车
    if (sb.is_element_visible('//*[@id="password"]')):
        sb.send_keys('//*[@id="password"]', Keys.ENTER)
    # sb.click('/html/body/div[1]/main/section/div/div/div/form/div[3]/button')

    # 等待登录完成
    wait_page_element('//*[@id="prompt-textarea"]', sb)

    # 切换到GPT-4
    wait_page_element('//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div[1]/div/div[2]', sb)
    sb.click('//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div[1]/div/div[2]')
    wait_page_element('//div[@class="flex grow items-center justify-between gap-2"]', sb)
    sb.click('//div[@class="flex grow items-center justify-between gap-2"]')

    wait_page_element('//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div/div[1]/div/div[2]', sb)

# chrome_options = Options()
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)

with SB(uc=True,headless=False, xvfb=True) as sb:
    login(sb)

