from utils.function_utils import *
from utils.path_utils import *

def checkCloudFlare(row,sb):
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
            except exceptions:
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
            except exceptions:
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
        except exceptions:
            passCloudFlare(row)
        except Exception:
            passCloudFlare(row)
    else:
        get_gpt_info(sb,row)
    
def get_gpt_info(sb,row):
    source_code = sb.get_page_source()
    bs = BeautifulSoup(source_code,"html.parser")
    title=bs.title
    if title is None:
        with open(os.path.join(GPTS_INFO_DIR, str(row[0])+"_"+row[2].split("/")[-1] + ".html"), mode='w', encoding='utf-8') as html_file:
            html_file.write("No page found")  
        print(row[0])
    else:
        title=title.get_text()
        if "Just a moment" in title:
            passCloudFlare(row)
        else:
            try:
                with open(os.path.join(GPTS_INFO_DIR, str(row[0])+"_"+row[2].split("/")[-1] + ".html"), mode='w', encoding='utf-8') as html_file:
                    html_file.write(source_code)
                print(row[0])
            except exceptions.NoSuchElementException:
                passCloudFlare(row)
            except exceptions.NoSuchFrameException:
                passCloudFlare(row)
            except exceptions.NoSuchWindowException:
                passCloudFlare(row)
            except exceptions:
                passCloudFlare(row)
            except Exception:
                passCloudFlare(row)

def passCloudFlare(row):
    with SB(uc_cdp=True, guest_mode=True) as sb:
        sb.open(GPTSTORE_URL+row[2])
        try:
            checkCloudFlare(row,sb)
        except exceptions.NoSuchElementException:
            passCloudFlare(row)
        except exceptions.NoSuchFrameException:
            passCloudFlare(row)
        except exceptions.NoSuchWindowException:
            passCloudFlare(row)
        except exceptions:
            passCloudFlare(row)
        except Exception:
            passCloudFlare(row)

if __name__ == "__main__":

    GPT_info_csv=os.path.join(DATA_DIR, 'allGPTs_index.csv')
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