import os
def listfile(userpath,endwithword='.txt'):
    f=[]
    for path,_,name in os.walk(userpath):
        for i in name:
            if i.endswith(endwithword):
                f.append(os.path.join(path,i))
    return f
if __name__=='__main__':
    print(listfile(os.getcwd()))
    

