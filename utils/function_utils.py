import json
from utils.function_utils import *
from bs4 import BeautifulSoup 

def data2csv(pddata,filename,index=False,col=True):
    pddata.to_csv(filename, sep=',', index=index,header=col)

