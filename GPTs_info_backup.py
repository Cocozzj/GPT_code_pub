from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import math
from seleniumbase import SB
import pandas as pd
import os
import sys
from bs4 import BeautifulSoup 

GPTStore_utl="https://gptstore.ai"
GPT_data="./Web_data/"
GPT_info_URL=GPT_data+"GPTs_info/"
GPT_info_csv=GPT_data+"allGPTs_index.csv"

def get_gpt_info(sb,row):
    source_code = sb.get_page_source()
    bs = BeautifulSoup(source_code,"html.parser")  
    title=bs.title.get_text()
    if "Just a moment" in title:
        passCloudFlare(row)
    else:
        with open(GPT_info_URL+str(row[0])+"_"+row[2].split("/")[-1] + ".html", mode='w', encoding='utf-8') as html_file:
            html_file.write(source_code)

def passCloudFlare(row):
    with SB(uc_cdp=True, guest_mode=False, locale_code="en_us") as sb:
        sb.open(GPTStore_utl+row[2])
        try:
            get_gpt_info(sb,row)
        except Exception:
            if sb.is_element_visible('input[value*="Verify"]'):
                sb.click('input[value*="Verify"]')
                time.sleep(3)
            elif sb.is_element_visible('iframe[title*="challenge"]'):
                sb.switch_to_frame('iframe[title*="challenge"]')
                sb.click("span.mark")
                time.sleep(3)
            else:
                raise Exception("Detected!")
            try:
                get_gpt_info(sb,row)
            except Exception:
                raise Exception("Detected!")

if __name__ == "__main__":

    df = pd.read_csv (GPT_info_csv)
    sys_argv_length=len(sys.argv)
    if sys_argv_length==2:
        df = df.iloc[int(sys.argv[1]):]
        for row in df.itertuples(name=None):
            passCloudFlare(row)
    elif sys_argv_length==3:
        df = df.iloc[int(sys.argv[1]):int(sys.argv[2])]

        for row in df.itertuples(name=None):
            passCloudFlare(row)
    else: 
        print("Please input <= 2 numbers")