import pandas as pd
import numpy as np
from part_type import part_type,rate_,name_
import os
from OP_ID import CB_OP_ID,CH_OP_ID


def collectall(database,wantID,typedetect):#迭代搜索所有装配子部件清单及数量，database是读取数据后的pandas表格，wantID是主动输入的希望查找的部件及其所有子装配部件。
    _finaldata=pd.DataFrame(columns=['part_id','father_id','relative_id','数量','订货号','型号','name','名称','OEM','类别','备注'])
    finaldata=[_finaldata]
    firstdata=database[database['father_id']==wantID]
    firstdata.apply(lambda x:appendson(x,1,database,finaldata,typedetect),axis=1)
    return finaldata[0]

def appendson(a,n,database,finaldata,typedetect):#迭代搜索子部件程序，子部件数量要和上级数量相乘
    a['数量']=int(a['数量'])*n
    _type=typedetect.get(str(a['订货号']))
    current_path = os.getcwd()
    if _type=='M':
        try:
            _path=r'\Data\M\{}.xlsx'.format(a['订货号'])
            _list=pd.read_excel(current_path+_path)
            _list['数量'] = _list['数量'] * a['数量']
            finaldata[0]=finaldata[0].append(_list,ignore_index=True,sort=False)
        except:
            print('找不到{}'.format(a['订货号']))
    elif _type=='F':
        try:
            _path=r'\Data\F\{}.xlsx'.format(a['订货号'])
            _list=pd.read_excel(current_path+_path)
            _list['数量']=_list['数量']*a['数量']
            finaldata[0]=finaldata[0].append(_list,ignore_index=True,sort=False)
        except:
            print('找不到{}'.format(a['订货号']))
    elif _type==None:
        finaldata[0]=finaldata[0].append(a,ignore_index=True,sort=False)
        if str(a['name']) in name_:
            print('cannot find {},{}'.format(a['型号'],a['名称']))
    else:
        a['类别']=_type
        finaldata[0]=finaldata[0].append(a,ignore_index=True,sort=False)
    if int(a['relative_id'])!=0:
        a1=database[database['father_id']==(int(a['relative_id'])+1)]
        a1.apply(lambda x:appendson(x,a['数量'],database,finaldata,typedetect),axis=1)
current_path = os.getcwd()
_cbdatapath=r'\database\CB_database.xlsx'
_chdatapath=r'\database\CH_database.xlsx'
try:
    cbdatabase=pd.read_excel(current_path+_cbdatapath)
    chdatabase=pd.read_excel(current_path+_chdatapath)
except:
    print("couldn't find data")
alldata=pd.DataFrame(columns=['part_id','father_id','relative_id','工位','数量','订货号','型号','name','名称','OEM','类别','备注'])
CBOP_Select=[]
CHOP_Select=['CH100A','CH120A','CH90A','CH100A']
alldata=collectall(cbdatabase,116,part_type)
alldata.to_excel('alldata.xlsx')
