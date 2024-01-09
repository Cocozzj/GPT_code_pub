from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.path_utils import *
from utils.function_utils import *
import json
import numpy as np
import requests
import time
API_KEY="e7d547d3def543d699dc0ea1cd6f9963"
url = "https://gpt-search-za6rvhzkqa-uc.a.run.app/"
headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

def get_allGPTs():
    response = requests.get(url+'gpts/count')
    counts=json.loads(response.text)
    count_num=int(counts['count'])
    print("Total GPT Num:"+ str(count_num))
    loop_num=int(np.ceil(count_num/100))
    print("Total index Num:"+ str(loop_num))

    data=[]
    for i in range(loop_num):
        skip=i*100
        response = requests.get(url+"gpts/?skip="+str(skip)+"&limit=100", headers=headers)
        response = json.loads(response.text)
        data.extend(response)

    data=pd.DataFrame(data)
    date=time.strftime("%Y-%m-%d", time.localtime()) 
    data2csv(data,date+'.csv') 

def match_GPT(filepath):
    GPT_info = pd.read_csv (filepath)
    gpt_id_list=GPT_info["openai_url"].values.tolist()
    response_list=[]
    for gpt_id in gpt_id_list:
        if isinstance(gpt_id,str):  
            gpt_id=gpt_id.split("/")[-1][2:]
            gpt_id=gpt_id.split("-")[0]
            response = requests.get(url+gpt_id, headers=headers)
            response = json.loads(response.text)
            
            response_list.append(response)

    response_list=pd.DataFrame(response_list)
    data2csv(response_list,'page_view_info.csv') 

if __name__ == "__main__":
    get_allGPTs()
