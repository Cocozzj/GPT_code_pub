from utils.function_utils import *
from utils.path_utils import *

GPT_INDEX_CSV= os.path.join(DATA_DIR, "allGPTs_index.csv")

def checkLength(start,end):
    list=[]
    for i in os.listdir(GPTS_INFO_DIR):
        list.append(int(i.split("_")[0]))
    list.sort()
    data=[]
    for i in range(start,end+1):
        if i in list:
            pass
        else:
            data.append(i)
    return data

def checkFormat():
    list=[]
    for i in os.listdir(GPTS_INFO_DIR):
        bs = BeautifulSoup(open(os.path.join(GPTS_INFO_DIR, i),encoding='utf-8'),features='html.parser') 
        title = bs.title
    if title is None:
        list.append(int(i.split("_")[0]))
    elif "GPTStore" in title.get_text():
        pass
    else:
        list.append(int(i.split("_")[0]))
    list.sort()
    return list

def reloadPage(list):
    if len(list)!=0:
        for tmp in list:
            print(tmp)
            df1 = df.iloc[tmp:tmp+1,:]
            for row in df1.itertuples(name=None):
                save_path=os.path.join(GPTS_INFO_DIR, str(row[0])+"_"+row[2].split("/")[-1] + ".html")
                passCloudFlare(GPTSTORE_URL+row[2],save_path,row[0])


if __name__ == "__main__":
    gpts_info_range=[1,10000]

    df = pd.read_csv(GPT_INDEX_CSV)
    list=checkLength(gpts_info_range[0],gpts_info_range[1])
    reloadPage(list)
    list=checkFormat()
    reloadPage(list)