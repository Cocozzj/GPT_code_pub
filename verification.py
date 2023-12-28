from utils.function_utils import *
from utils.path_utils import *
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


GPT_INDEX_CSV= os.path.join(DATA_DIR, "allGPTs_index.csv")

def checkLength(start,end):
    list=[]
    for i in os.listdir(GPTS_INFO_DIR):
        list.append(int(i.split("_")[0]))
    list.sort()
    data=[]
    for i in range(start,end+1):
        if i in list:
            pass
        else:
            data.append(i)
    return data

def checkFormat():
    list=[]
    for i in os.listdir(GPTS_INFO_DIR):
        bs = BeautifulSoup(open(os.path.join(GPTS_INFO_DIR, i),encoding='utf-8'),features='html.parser')
        
        title = bs.title
        if title is None:
            list.append(int(i.split("_")[0]))
        elif "GPTStore" in title.get_text():
            pass
        else:
            list.append(int(i.split("_")[0]))
    list.sort()
    return list

def get_gpt_info(url,save_path,index):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9224")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    driver.set_window_size(200,800) 

    driver.get(url)
    time.sleep(1)
    source_code=driver.page_source
    if "Just a moment" in driver.title:
        print(str(index)+"verify cloudflare")
        sys.exit(0)
    else:
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

def reloadPage(list):
    if len(list)!=0:
        for tmp in list:
            # print(tmp)
            df1 = df.iloc[tmp:tmp+1,:]
            for row in df1.itertuples(name=None):
                save_path=os.path.join(GPTS_INFO_DIR, str(row[0])+"_"+row[2] + ".html")
                get_gpt_info(row[3],save_path,row[0])

if __name__ == "__main__":
    
    df = pd.read_csv(GPT_INDEX_CSV)

    gpts_info_range=[0,len(df)-1]
    list=checkLength(gpts_info_range[0],gpts_info_range[1])
    print(list)
    reloadPage(list)
    list=checkFormat()
    print(list)
    reloadPage(list)