from utils.function_utils import *
from utils.path_utils import *

def get_page_num(bs,key):
    print("############## "+key+" ##############")
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
        passCloudFlare(url+"?page="+str(page_id),save_path,page_id,False)


def goto_category_page(key,url):
    with SB(uc_cdp=True, guest_mode=True) as sb:
        sb.open(url)
        try:
            source_code = sb.get_page_source()
            bs = BeautifulSoup(source_code,"html.parser")  
            title=bs.title.get_text()
            if "Just a moment" in title:
                if sb.is_element_visible('input[value*="Verify"]'):
                    sb.click('input[value*="Verify"]')
                elif sb.is_element_visible('iframe[title*="challenge"]'):
                    sb.switch_to_frame('iframe[title*="challenge"]')
                    sb.click("span.mark")  
                # else:
                #     goto_category_page(url)
            time.sleep(1)
            
            page_num=get_page_num(bs,key)
                
        # except exceptions.NoSuchElementException:
        #     goto_category_page(key,url)
        # except exceptions.NoSuchFrameException:
        #     goto_category_page(key,url)
        # except exceptions.NoSuchWindowException:
        #     goto_category_page(key,url)
        except Exception:
            sb.driver.quit()
            goto_category_page(key,url)

    return page_num

####################### Get GPTs index in category#########################

GPT_info_csv=os.path.join(DATA_DIR, 'category_index.csv')
category_list = pd.read_csv (GPT_info_csv)
category_list=category_list.iloc[46:]
for row in category_list.itertuples():
    key=row[2]
    url=row[3]
    page_num=goto_category_page(key,url)
    get_category_page(page_num,key,url)
    
    