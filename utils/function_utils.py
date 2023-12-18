
def data2csv(pddata,filename,index=False,col=True):
    pddata.to_csv(filename, sep=',', index=index,header=col)
    