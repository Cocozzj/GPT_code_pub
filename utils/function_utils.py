from selenium.common import exceptions
import time
import json
from seleniumbase import SB
from bs4 import BeautifulSoup 
from utils.function_utils import *

def data2csv(pddata,filename,index=False,col=True):
    pddata.to_csv(filename, sep=',', index=index,header=col)


