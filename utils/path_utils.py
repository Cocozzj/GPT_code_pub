import os
import sys
import pandas as pd

def notExist_create(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)

GPTSTORE_URL="https://gptstore.ai/"
GPTS_NUM_PERPAGE=15
PROJ_DIR =os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(PROJ_DIR)
DATA_DIR=os.path.join(PROJ_DIR, 'Web_data')
GPTS_INFO_DIR=os.path.join(DATA_DIR, 'GPTs_info')
GPTS_INDEX_DIR=os.path.join(DATA_DIR, 'GPTs_index')
CATEGORY_INDEX_DIR=os.path.join(DATA_DIR, 'Category_index')

notExist_create(GPTS_INFO_DIR)
notExist_create(GPTS_INDEX_DIR)
notExist_create(CATEGORY_INDEX_DIR)