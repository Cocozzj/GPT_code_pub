from utils.path_utils import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from bs4 import BeautifulSoup 

def get_page_num(key,url):
    print("############## "+key+" ##############")
    driver.get(url)
    time.sleep(3)
    source_code=driver.page_source
    bs = BeautifulSoup(source_code,"html.parser")
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
    bs = BeautifulSoup(source_code,"html.parser")
    title=bs.title
    if title is None:
        with open(save_path, mode='w', encoding='utf-8') as html_file:
            html_file.write("No page found")  
    else:
        title=title.get_text()
        if "GPTStore" in title:
            with open(save_path, mode='w', encoding='utf-8') as html_file:
                html_file.write(source_code)
                time.sleep(1)
        elif "gptstore.ai" == title:
            with open(save_path, mode='w', encoding='utf-8') as html_file:
                html_file.write("No page found")
        else: 
            driver.refresh()
    print(page_id)
 


####################### Get GPTs index in category#########################
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
driver = webdriver.Chrome(options=chrome_options)

GPT_info_csv=os.path.join(DATA_DIR, 'category_index.csv')
category_list = pd.read_csv (GPT_info_csv)
# category_list=category_list.iloc[1:]
for row in category_list.itertuples():
    key=row[2]
    url=row[3]
    
    page_num=get_page_num(key,url)
    get_category_page(page_num,key,url)
    
    