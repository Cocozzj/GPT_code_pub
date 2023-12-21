from selenium.common import exceptions
import time
import json
from seleniumbase import SB
from bs4 import BeautifulSoup 
from utils.function_utils import *

def data2csv(pddata,filename,index=False,col=True):
    pddata.to_csv(filename, sep=',', index=index,header=col)

def checkCloudFlare(sb,url,save_path,index,updatebutton):
    source_code = sb.get_page_source()
    bs = BeautifulSoup(source_code,"html.parser")  
    title=bs.title.get_text()
    if "Just a moment" in title:
        time.sleep(1) 
        if sb.is_element_visible('input[value*="Verify"]'):
            sb.click('input[value*="Verify"]')
        elif sb.is_element_visible('iframe[title*="challenge"]'):
            sb.switch_to_frame('iframe[title*="challenge"]')
            sb.click("span.mark")
        # else:
        #     print("ZZZZZZZ")
        #     sb.driver.quit()
        #     passCloudFlare(url,save_path,index) 
    get_gpt_info(sb,url,save_path,index,updatebutton)
    
    
def get_gpt_info(sb,url,save_path,index,updatebutton):
    time.sleep(1)
    source_code = sb.get_page_source()
    bs = BeautifulSoup(source_code,"html.parser")
    title=bs.title
    if title is None:
        with open(save_path, mode='w', encoding='utf-8') as html_file:
            html_file.write("No page found")  
        print(index)
    else:
        title=title.get_text()
        if "GPTStore" in title:
            with open(save_path, mode='w', encoding='utf-8') as html_file:
                html_file.write(source_code)
                print(index)
            #print(sb.is_attribute_present('#__next > main > div.space-y-3 > div.flex.justify-center.gap-x-6 > button','disabled'))
            # if sb.is_element_visible('#__next > main > div.space-y-3 > div.flex.justify-center.gap-x-6 > button'):
            #     break
            if updatebutton:           
                if sb.is_element_visible('#__next > main > div.mt-4.space-y-4 > div > div.mt-6 > dl > div.flex.items-center.border-t.border-gray-100.py-6.dark\:border-gray-900.sm\:col-span-1 > dd > button'):
                    sb.click('#__next > main > div.mt-4.space-y-4 > div > div.mt-6 > dl > div.flex.items-center.border-t.border-gray-100.py-6.dark\:border-gray-900.sm\:col-span-1 > dd > button')
                    print(index)
                    time.sleep(1)
            else:
                print(index)
        else: 
            sb.driver.quit()
            passCloudFlare(url,save_path,index,updatebutton)

def passCloudFlare(url,save_path,index,updatebutton=True):
    with SB(uc_cdp=True, guest_mode=True,locale_code="en_us",headless=False) as sb:
        sb.open(url)
        try:
            checkCloudFlare(sb,url,save_path,index,updatebutton)
        # except exceptions.NoSuchElementException:
        #     passCloudFlare(url,save_path,index)
        # except exceptions.NoSuchFrameException:
        #     passCloudFlare(url,save_path,index)
        # except exceptions.NoSuchWindowException:
        #     passCloudFlare(url,save_path,index)
        except Exception:
            sb.driver.quit()
            passCloudFlare(url,save_path,index,updatebutton)


