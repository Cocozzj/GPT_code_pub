from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import math
from seleniumbase import SB
from bs4 import BeautifulSoup 
import pandas as pd
from utils.path_utils import *
from utils.function_utils import *

gpt_num_url='//div[@id="__next"]/main/div[1]/div/p'
category_url='//div[@id="__next"]/main/div[2]/div[1]/div/div'

element=["gpts","creators","plugins"]

GPTs_url=GPTSTORE_URL+element[0]
print(GPTs_url)
# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument('--save-page-as-mhtml')
# options.add_argument('--disable-blink-features=AutomationControlled')
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()

####################### Get GPTs Category List #########################
driver.get(GPTs_url)
category_button=driver.find_element(By.XPATH,category_url+'/div[1]/button')
category_button.click()
category_list1=[]
category_list2=[]
category_default=driver.find_elements(By.XPATH,category_url+'/div[1]/div/a')
for i in category_default:
    category_list1.append([i.text,i.get_attribute('href')])
category_extend=driver.find_elements(By.XPATH,category_url+'/div[2]/a')
for i in category_extend:
    category_list2.append([i.text,i.get_attribute('href')])
category_list=category_list1+category_list2

print(category_list)

gpt_info=pd.DataFrame(category_list,columns =['name', 'url'])

data2csv(gpt_info,os.path.join(DATA_DIR, 'category_index.csv')) 


####################### Get Total Num of GPTs #########################

gpts_num_str=driver.find_elements(By.XPATH,gpt_num_url)
gpts_num_str=gpts_num_str[0].text
gpts_num=int(gpts_num_str.split(" ")[3])
page_num = math.ceil(gpts_num/GPTS_NUM_PERPAGE)

print("Total # GPTs: "+ str(gpts_num))
print("Total # GPTs page: "+str(page_num))

####################### Get All GPTs info#########################

gpt_index=[]
for page_id in range(1, page_num+1):
    print(page_id)
    driver.get(GPTs_url+"?page="+str(page_id))
    source_code = driver.page_source
    save_path=os.path.join(GPTS_INDEX_DIR, str(page_id)+ ".html")
    with open(save_path, mode='w', encoding='utf-8') as html_file:
        html_file.write(source_code)
####################### summary All GPTs name+url#########################



file_num= len(os.listdir(GPTS_INDEX_DIR))
gpt_info=[]

for num in range(1,file_num+1):
    file = open(GPTS_INDEX_DIR+str(num)+'.html', 'rb') 
    html = file.read() 
    bs = BeautifulSoup(html,"html.parser")   
    for list in bs.find_all("li"):
        gpt_name=list.a.get_text()
        gpt_url=list.a.get("href")
        gpt_info.append([gpt_name,gpt_url])

gpt_info=pd.DataFrame(gpt_info,columns =['name', 'url'])

data2csv(gpt_info,os.path.join(DATA_DIR, 'allGPTs_index.csv')) 