from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils.path_utils import *
from utils.function_utils import *
import json
import time
element=["gpts","creators","plugins"]

GPTs_url=GPTSTORE_URL+element[0]
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=chrome_options)


####################### Get GPTs Category List #########################
driver.get(GPTs_url)

json_html=driver.find_element(By.XPATH,'//*[@id="__NEXT_DATA__"]').get_attribute("innerHTML")
json_html = json.loads(json_html)

gpts=json_html["props"]["pageProps"]

category_list=[]
gptCategoryList=gpts["gptCategoryList"]
for index in gptCategoryList:
    category_list.append([index["id"],index["category"],GPTs_url+"/categories/"+str.lower(index["category"].replace(" ","-"))])

gpt_info=pd.DataFrame(category_list,columns =['id','name','url'])

data2csv(gpt_info,os.path.join(DATA_DIR, 'category_index.csv')) 

# # ####################### Get Total Num of GPTs #########################

gpts_num=gpts["count"]
page_num=gpts["total"]

print("Total # GPTs: "+ str(gpts_num))
print("Total # GPTs page: "+str(page_num))

# # # ####################### Get All GPTs info#########################

def reload(driver,page_id):
    
    if len(driver.find_elements(By.XPATH,'/html/body/pre'))>0:
        print(str(index)+":Reload")
        driver.get(GPTs_url+"?page="+str(page_id))
        flag=True
    else:
        flag=False
    # print(flag)
    return flag

gpt_index=[]
for page_id in range(4644, page_num+2):
    driver.get(GPTs_url+"?page="+str(page_id))
    flag=True
    while(flag):
        flag=reload(driver,page_id)
    source_code = driver.page_source
    save_path=os.path.join(GPTS_INDEX_DIR, str(page_id)+ ".html")
    with open(save_path, mode='w', encoding='utf-8') as html_file:
        html_file.write(source_code)
    print(page_id)
    

# ####################### summary All GPTs name+url#########################

file_num= len(os.listdir(GPTS_INDEX_DIR))
# print(file_num)
gpt_info=[]

for num in range(1,file_num+1):
    file = open(os.path.join(GPTS_INDEX_DIR, str(num)+ ".html"), 'rb') 
    html = file.read() 
    bs = BeautifulSoup(html,"html.parser")   
    for list in bs.find_all("li"):
        gpt_name=list.a.get_text()
        gpt_url=list.a.get("href")
        gpt_id=gpt_url[6:]
        gpt_count=list.select("div")[-1]
        
        gpt_info.append([gpt_name,gpt_id,GPTs_url+"/"+gpt_id])


gpt_info=pd.DataFrame(gpt_info,columns =['name', 'id','url'])



data2csv(gpt_info,os.path.join(DATA_DIR, 'allGPTs_index.csv')) 