from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import math
from seleniumbase import SB
import os
import pandas as pd
from bs4 import BeautifulSoup 

URL="https://gptstore.ai/"
GPTS_NUM_PERPAGE=15
GPT_data="./Web_data/"
category_index_URL=GPT_data+"category_index/"
category_url='//div[@id="__next"]/main/div[2]/div[1]/div/div'

element=["gpts","creators","plugins"]

def data2csv(pddata,filename,index=False,col=True):
    pddata.to_csv(filename, sep=',', index=index,header=col)


def get_gpts_num(sb):
    gpts_num_str=sb.get_text("#__next main div div p")
    gpt_num=int(gpts_num_str.split(" ")[3])
    return gpt_num

def open_page(sb,key):
    print("############## "+key+" ##############")
    gpts_num=get_gpts_num(sb)
    page_num=math.ceil(gpts_num/GPTS_NUM_PERPAGE)
    print("# GPTs: "+ str(gpts_num))
    print("# GPTs page: "+str(page_num))
    return page_num  

def verify_success(url,save_path,page_id,sb):
    source_code = sb.get_page_source()
    bs = BeautifulSoup(source_code,"html.parser")  
    title=bs.title.get_text()
    if "Just a moment" in title:
        passCloudFlare(url,save_path,page_id)
    else:
        print(page_id)
        with open(save_path+str(page_id) + ".html", mode='w', encoding='utf-8') as html_file:
            html_file.write(source_code)
 
    
def passCloudFlare(url,save_path,page_id):
    with SB(uc_cdp=True, guest_mode=True) as sb:
        sb.open(url)
        try:
            verify_success(url,save_path,page_id,sb)
        except Exception:
            if sb.is_element_visible('input[value*="Verify"]'):
                sb.click('input[value*="Verify"]')
                time.sleep(1)
            elif sb.is_element_visible('iframe[title*="challenge"]'):
                sb.switch_to_frame('iframe[title*="challenge"]')
                sb.click("span.mark")
                time.sleep(1)
            else:
                raise Exception("Detected!")
            try:
                verify_success(url,save_path,page_id,sb)
            except Exception:
                raise Exception("Detected!")
            

def get_category_page(sb,key):
    page_num = open_page(sb,key)
    save_path=category_index_URL+key+"/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for page_id in range(1, page_num+1):
        passCloudFlare(link+"?page="+str(page_id),save_path,page_id)




####################### Get GPTs index in category#########################
for key, link in category_list:
    with SB(uc_cdp=True, guest_mode=True) as sb:
        sb.open(link)
        try:
            get_category_page(sb,key)
        except Exception:
            if sb.is_element_visible('input[value*="Verify"]'):
                sb.click('input[value*="Verify"]')
                time.sleep(1)
            elif sb.is_element_visible('iframe[title*="challenge"]'):
                sb.switch_to_frame('iframe[title*="challenge"]')
                sb.click("span.mark")
                time.sleep(1)
            else:
                raise Exception("Detected!")
            try:
                get_category_page(sb,key)
            except Exception:
                raise Exception("Detected!")
    