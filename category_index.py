from utils.path_utils import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from bs4 import BeautifulSoup 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_page_num(key,url,index):
    print("############## "+str(index)+" : "+key+" ##############")
    driver.get(url)
    if "Just a moment" in driver.title:
        print(key+" :verify cloudflare")
        sys.exit(0)
    else:
        source_code=driver.page_source
        bs = BeautifulSoup(source_code,"html.parser")
        if len(bs.find_all(id='__NEXT_DATA__'))<1:
            get_page_num(key,url)
        else:
            json_html=bs.find_all(id='__NEXT_DATA__')[0].get_text()
            json_html = json.loads(json_html)
            gpts=json_html["props"]["pageProps"]
            gpts_num=int(gpts["count"])
            page_num=int(gpts["total"])
            print("# GPTs: "+ str(gpts_num))
            print("# GPTs page: "+str(page_num))

    return page_num  
            
def get_category_page(page_num,key,url):
    category_path=os.path.join(CATEGORY_INDEX_DIR, key)
    notExist_create(category_path)
    for page_id in range(1, page_num+1):
        save_path= os.path.join(category_path,str(page_id) + ".html")
        getGPTs_info(url+"?page="+str(page_id),save_path,page_id)

def getGPTs_info(url,save_path,page_id):
    driver.get(url)
    time.sleep(1)
    source_code=driver.page_source
    if "Just a moment" in driver.title:
        print(str(page_id)+"verify cloudflare")
        sys.exit(0)
    else:
        if "GPTStore" in driver.title:
            with open(save_path, mode='w', encoding='utf-8') as html_file:
                html_file.write(source_code)  
            print(page_id)
        else:
            print(str(page_id)+":No page found")
            getGPTs_info(url,save_path,page_id)
  
 

####################### Get GPTs index in category#########################
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=chrome_options)

GPT_info_csv=os.path.join(DATA_DIR, 'category_index.csv')
category_list = pd.read_csv (GPT_info_csv)
category_list=category_list.iloc[31:]
for row in category_list.itertuples():
    key=row[2]
    url=row[3]
    page_num=get_page_num(key,url,row[0])
    get_category_page(page_num,key,url)
    
    