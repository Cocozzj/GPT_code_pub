from utils.function_utils import *
from utils.path_utils import *

def get_page_num(sb,key):
    print("############## "+key+" ##############")
    gpts_num_str=sb.get_text("#__next main div div p")
    gpt_num=int(gpts_num_str.split(" ")[3])
    page_num=math.ceil(gpt_num/GPTS_NUM_PERPAGE)
    print("# GPTs: "+ str(gpt_num))
    print("# GPTs page: "+str(page_num))
    return page_num  

def verify_success(url,save_path,page_id,sb):
    source_code = sb.get_page_source()
    bs = BeautifulSoup(source_code,"html.parser")  
    title=bs.title.get_text()
    if "Just a moment" in title:
        passCloudFlare(url,save_path,page_id)
    else:    
        with open(os.path.join(save_path, str(page_id) + ".html"), mode='w', encoding='utf-8') as html_file:
            html_file.write(source_code)
        print(page_id)
 
    
def passCloudFlare(url,save_path,page_id):
    with SB(uc_cdp=True, guest_mode=True) as sb:
        sb.open(url)
        try:
            checkCloudFlare(sb,save_path,page_id)
        except exceptions.NoSuchElementException:
            passCloudFlare(url,save_path,page_id)
        except exceptions.NoSuchFrameException:
            passCloudFlare(url,save_path,page_id)
        except exceptions.NoSuchWindowException:
            passCloudFlare(url,save_path,page_id)
        except exceptions:
            passCloudFlare(url,save_path,page_id)
        except Exception:
            passCloudFlare(url,save_path,page_id)


def checkCloudFlare(sb,save_path,page_id):
    source_code = sb.get_page_source()
    bs = BeautifulSoup(source_code,"html.parser")  
    title=bs.title.get_text()
    if "Just a moment" in title:
        if sb.is_element_visible('input[value*="Verify"]'):
            try:
                sb.click('input[value*="Verify"]')
            except exceptions.NoSuchElementException:
                passCloudFlare(url,save_path,page_id)
            except exceptions.NoSuchFrameException:
                passCloudFlare(url,save_path,page_id)
            except exceptions.NoSuchWindowException:
                passCloudFlare(url,save_path,page_id)
            except exceptions:
                passCloudFlare(url,save_path,page_id)
            except Exception:
                passCloudFlare(url,save_path,page_id)
        elif sb.is_element_visible('iframe[title*="challenge"]'):
            try:
                sb.switch_to_frame('iframe[title*="challenge"]')
                sb.click("span.mark")
                time.sleep(1)  
            except exceptions.NoSuchElementException:
                passCloudFlare(url,save_path,page_id)
            except exceptions.NoSuchFrameException:
                passCloudFlare(url,save_path,page_id)
            except exceptions.NoSuchWindowException:
                passCloudFlare(url,save_path,page_id)
            except exceptions:
                passCloudFlare(url,save_path,page_id)
            except Exception:
                passCloudFlare(url,save_path,page_id)
        else:
            # raise Exception("Detected!")
            passCloudFlare(url,save_path,page_id)
        try:
            verify_success(url,save_path,page_id,sb)
        except exceptions.NoSuchElementException:
            passCloudFlare(url,save_path,page_id)
        except exceptions.NoSuchFrameException:
            passCloudFlare(url,save_path,page_id)
        except exceptions.NoSuchWindowException:
            passCloudFlare(url,save_path,page_id)
        except exceptions:
            passCloudFlare(url,save_path,page_id)
        except Exception:
            passCloudFlare(url,save_path,page_id)
    else:
        verify_success(url,save_path,page_id,sb)
            

def get_category_page(page_num,key,url):
    save_path= os.path.join(CATEGORY_INDEX_DIR, key)
    for page_id in range(1, page_num+1):
        passCloudFlare(url+"?page="+str(page_id),save_path,page_id)


def goto_category_page(key,url):
    with SB(uc_cdp=True, guest_mode=True) as sb:
        sb.open(url)
        try:
            source_code = sb.get_page_source()
            bs = BeautifulSoup(source_code,"html.parser")  
            title=bs.title.get_text()
            if "Just a moment" in title:
                if sb.is_element_visible('input[value*="Verify"]'):
                    try:
                        sb.click('input[value*="Verify"]')
                    except exceptions.NoSuchElementException:
                        goto_category_page(url)
                    except exceptions.NoSuchFrameException:
                        goto_category_page(url)
                    except exceptions.NoSuchWindowException:
                        goto_category_page(url)
                    except exceptions:
                        goto_category_page(url)
                    except Exception:
                        goto_category_page(url)
                elif sb.is_element_visible('iframe[title*="challenge"]'):
                    try:
                        sb.switch_to_frame('iframe[title*="challenge"]')
                        sb.click("span.mark")  
                    except exceptions.NoSuchElementException:
                        goto_category_page(url)
                    except exceptions.NoSuchFrameException:
                        goto_category_page(url)
                    except exceptions.NoSuchWindowException:
                        goto_category_page(url)
                    except exceptions:
                        goto_category_page(url)
                    except Exception:
                        goto_category_page(url)
                else:
                    goto_category_page(url)
                try:
                    page_num=get_page_num(sb,key)
                    get_category_page(page_num,key,url)
                except exceptions.NoSuchElementException:
                        goto_category_page(url)
                except exceptions.NoSuchFrameException:
                    goto_category_page(url)
                except exceptions.NoSuchWindowException:
                    goto_category_page(url)
                except exceptions:
                    goto_category_page(url)
                except Exception:
                    goto_category_page(url)
            else:
                page_num=get_page_num(sb,key)
                get_category_page(page_num,key,url)
        except exceptions.NoSuchElementException:
            goto_category_page(url)
        except exceptions.NoSuchFrameException:
            goto_category_page(url)
        except exceptions.NoSuchWindowException:
            goto_category_page(url)
        except exceptions:
            goto_category_page(url)
        except Exception:
            goto_category_page(url)


####################### Get GPTs index in category#########################
        
GPT_info_csv=os.path.join(DATA_DIR, 'category_index.csv')
category_list = pd.read_csv (GPT_info_csv)

for row in category_list.itertuples():
    key=row[1]
    url=row[2]
    goto_category_page(key,url)
    # print("############## "+key+" ##############")
    # with SB(uc_cdp=True, guest_mode=True) as sb:
    #     sb.open(link)
    #     try:
    #         get_category_page(sb,key)
    #     except Exception:
    #         if sb.is_element_visible('input[value*="Verify"]'):
    #             sb.click('input[value*="Verify"]')
    #             time.sleep(1)
    #         elif sb.is_element_visible('iframe[title*="challenge"]'):
    #             sb.switch_to_frame('iframe[title*="challenge"]')
    #             sb.click("span.mark")
    #             time.sleep(1)
    #         else:
    #             raise Exception("Detected!")
    #         try:
    #             get_category_page(sb,key)
    #         except Exception:
    #             raise Exception("Detected!")
    