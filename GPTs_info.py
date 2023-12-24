from utils.function_utils import *
from utils.path_utils import *

GPT_INDEX_CSV= os.path.join(DATA_DIR, "allGPTs_index.csv")

if __name__ == "__main__":
    df = pd.read_csv (GPT_INDEX_CSV)
    sys_argv_length=len(sys.argv)
    if sys_argv_length==2:
        df = df.iloc[int(sys.argv[1]):]
        for row in df.itertuples(name=None):
            save_path=os.path.join(GPTS_INFO_DIR, str(row[0])+"_"+row[2] + ".html")
            passCloudFlare(row[3],save_path,row[0])
    elif sys_argv_length==3:
        if sys.argv[1]==sys.argv[2]:
            df = df.iloc[int(sys.argv[1]):int(sys.argv[1])+1,:]
        else:
            df = df.iloc[int(sys.argv[1]):int(sys.argv[2])+1]
            for row in df.itertuples(name=None):
                save_path=os.path.join(GPTS_INFO_DIR, str(row[0])+"_"+row[2] + ".html")
                passCloudFlare(row[3],save_path,row[0])
    else: 
        print("Please input <= 2 numbers")