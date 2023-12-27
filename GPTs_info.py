from utils.path_utils import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


GPT_INDEX_CSV= os.path.join(DATA_DIR, "allGPTs_index.csv")

def get_gpt_info(url,save_path,index):
    driver.get(url)
    time.sleep(1)
    source_code=driver.page_source
    with open(save_path, mode='w', encoding='utf-8') as html_file:
        html_file.write(source_code)  
    if "GPTStore" in driver.title:
        updateRequest=driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[2]/div[1]/div[1]/div[2]/dl/div[4]/dd/button')
        if (updateRequest.is_enabled()):
            updateRequest.click()
            print(index)
        else:
            print(str(index)+":Can not update request")
    else:
        print(str(index)+":No page found")


if __name__ == "__main__":

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)

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