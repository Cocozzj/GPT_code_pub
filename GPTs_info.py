from utils.path_utils import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys

GPT_INDEX_CSV= os.path.join(DATA_DIR, "allGPTs_index.csv")

def passcloudflare(driver,url,save_path,index):
    # ele1= driver.find_element(By.XPATH,'//*[@id="challenge-stage"]'
    try:
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='Widget containing a Cloudflare security challenge']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@class='ctp-checkbox-label']"))).click()
        time.sleep(60)
    except Exception:
        get_gpt_info(url,save_path,index)
    # ele1= driver.find_elements(By.CSS_SELECTOR, 'input[value*="Verify"]')
    # ele2 =driver.find_elements(By.CSS_SELECTOR, 'iframe[title*="challenge"]')
    # time.sleep(1)
    # if len(ele1)>0:
    #     driver.find_element(By.CSS_SELECTOR,'input[value*="Verify"]').click()
    # elif len(ele2)>0:
    #     driver.switch_to.frame(ele2[0])
    #     sb=driver.find_elements(By.TAG_NAME,'label')
    #     time.sleep(1)
    #     sb.click()   
    # else:
    #     get_gpt_info(url,save_path,index)


def get_gpt_info(url,save_path,index):
    try:
        driver.get(url)
        time.sleep(1)
        if "Just a moment" in driver.title:
            print(str(index)+"verify cloudflare")
            sys.exit(0)
            # try:
            #     passcloudflare(driver,url,save_path,index)
            # except Exception:
            #     raise("Detect")
            # get_gpt_info(url,save_path,index)
        elif len(driver.find_elements(By.XPATH,'/html/body/pre'))>0:
            get_gpt_info(url,save_path,index)
            print(str(index)+":Reload")
        else:
            source_code=driver.page_source
            with open(save_path, mode='w', encoding='utf-8') as html_file:
                html_file.write(source_code) 
        
            if "GPTStore" in driver.title:
                updateRequest=driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[2]/div[1]/div[1]/div[2]/dl/div[4]/dd/button')
                if (updateRequest.is_enabled()):
                    updateRequest.click()
                    print(index)
                else:
                    print("Can not update request")
            else:
                print(str(index)+":No page found")
    except TimeoutException:
        print("TimeoutException")
        driver.refresh()
        # driver.get('chrome://settings/clearBrowserData')
        # driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
        get_gpt_info(url,save_path,index)
    


if __name__ == "__main__":
   
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    driver.set_window_size(200,800) 

    df = pd.read_csv (GPT_INDEX_CSV)
    sys_argv_length=len(sys.argv)
    if sys_argv_length==2:
        df = df.iloc[int(sys.argv[1]):]
        for row in df.itertuples(name=None):
            save_path=os.path.join(GPTS_INFO_DIR, str(row[0])+"_"+row[2] + ".html")
            get_gpt_info(row[3],save_path,row[0])
    elif sys_argv_length==3:
        if sys.argv[1]==sys.argv[2]:
            df = df.iloc[int(sys.argv[1]):int(sys.argv[1])+1,:]
        else:
            df = df.iloc[int(sys.argv[1]):int(sys.argv[2])+1]
            for row in df.itertuples(name=None):
                save_path=os.path.join(GPTS_INFO_DIR, str(row[0])+"_"+row[2] + ".html")
                get_gpt_info(row[3],save_path,row[0])
    else: 
        print("Please input <= 2 numbers")