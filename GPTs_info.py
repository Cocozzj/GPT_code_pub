import time
import math
from seleniumbase import SB
import pandas as pd
import os
from bs4 import BeautifulSoup 
from selenium.common import exceptions

tmp=[25000,25017]
GPTStore_utl="https://gptstore.ai"
GPT_data="./Web_data/"
GPT_info_URL=GPT_data+"GPTs_info/"
if not os.path.exists(GPT_info_URL):
    os.makedirs(GPT_info_URL)
GPT_info_csv=GPT_data+"allGPTs_index.csv"

def checkCloudFlare(sb):
    source_code = sb.get_page_source()
    bs = BeautifulSoup(source_code,"html.parser")  
    title=bs.title.get_text()
    if "Just a moment" in title:
        if sb.is_element_visible('input[value*="Verify"]'):
            try:
                sb.click('input[value*="Verify"]')
            except exceptions.NoSuchElementException:
                passCloudFlare(row)
            except exceptions.NoSuchFrameException:
                passCloudFlare(row)
            except exceptions.NoSuchWindowException:
                passCloudFlare(row)
            except Exception:
                passCloudFlare(row)
        elif sb.is_element_visible('iframe[title*="challenge"]'):
            try:
                sb.switch_to_frame('iframe[title*="challenge"]')
                sb.click("span.mark")
                time.sleep(1)  
            except exceptions.NoSuchElementException:
                passCloudFlare(row)
            except exceptions.NoSuchFrameException:
                passCloudFlare(row)
            except exceptions.NoSuchWindowException:
                passCloudFlare(row)
            except Exception:
                passCloudFlare(row)
        else:
            # raise Exception("Detected!")
            passCloudFlare(row)
        try:
            get_gpt_info(sb,row)
        except exceptions.NoSuchElementException:
            passCloudFlare(row)
        except exceptions.NoSuchFrameException:
            passCloudFlare(row)
        except exceptions.NoSuchWindowException:
            passCloudFlare(row)
        except Exception:
            passCloudFlare(row)
    else:
        get_gpt_info(sb,row)
    
def get_gpt_info(sb,row):
    source_code = sb.get_page_source()
    bs = BeautifulSoup(source_code,"html.parser")  
    title=bs.title.get_text()
    if "Just a moment" in title:
        passCloudFlare(row)
    else:
        try:
            print(row[0])
            with open(GPT_info_URL+str(row[0])+"_"+row[2].split("/")[-1] + ".html", mode='w', encoding='utf-8') as html_file:
                html_file.write(source_code)
        except exceptions.NoSuchElementException:
            passCloudFlare(row)
        except exceptions.NoSuchFrameException:
            passCloudFlare(row)
        except exceptions.NoSuchWindowException:
            passCloudFlare(row)
        except Exception:
            passCloudFlare(row)

def passCloudFlare(row):
    with SB(uc_cdp=True, guest_mode=True) as sb:
        sb.open(GPTStore_utl+row[2])
        try:
            checkCloudFlare(sb)
        # except exceptions:
        #     sb.refresh()
        except exceptions.NoSuchElementException:
            passCloudFlare(row)
        except exceptions.NoSuchFrameException:
            passCloudFlare(row)
        except exceptions.NoSuchWindowException:
            passCloudFlare(row)
        except Exception:
            passCloudFlare(row)
        

df = pd.read_csv (GPT_info_csv)

df = df.iloc[tmp[0]:tmp[1]]
for row in df.itertuples(name=None):
    passCloudFlare(row)