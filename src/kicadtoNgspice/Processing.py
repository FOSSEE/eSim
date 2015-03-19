
class PrcocessNetlist:
    def __init__(self):
        pass
    
    def readNetlist(self,filename):
        f = open(filename)
        data=f.read()
        f.close()
        return data.splitlines()
