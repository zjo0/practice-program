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
        if int(a['relative_id'])!=0:
            a1=database[database['father_id']==(int(a['relative_id'])+1)]
            a1.apply(lambda x:appendson(x,a['数量'],database,finaldata,typedetect),axis=1)
    else:
        b=a.copy()
        b['类别']=_type
        finaldata[0]=finaldata[0].append(b,ignore_index=True,sort=False)
current_path = os.getcwd()
_cbdatapath=r'\database\CB_database.xlsx'
_chdatapath=r'\database\CH_database.xlsx'
try:
    cbdatabase=pd.read_excel(current_path+_cbdatapath)
    chdatabase=pd.read_excel(current_path+_chdatapath)
except:
    print("couldn't find data")
alldata=pd.DataFrame(columns=['part_id','father_id','relative_id','工位','数量','订货号','型号','name','名称','OEM','类别','备注'])
CBOP_Select=['CB10A','CB30A','CB40A','CB40C','CB50A','CB130A','CB130B','CB130C','CB130D']
CHOP_Select=['CH10C','CH20A','CH20C','CH30A','CH40A','CH50A','CH110A','CH120A','CH120B','CH120C','CH120D']
for i in CBOP_Select:
    print('search {}'.format(i))
    wantID=CB_OP_ID[i]
    a=collectall(cbdatabase,wantID,part_type)
    a=a.dropna(subset=['类别'])
    a['工位']=i
    alldata=alldata.append(a,ignore_index=True,sort=False)
for i in CHOP_Select:
    print('search {}'.format(i))
    wantID=CH_OP_ID[i]
    a=collectall(chdatabase,wantID,part_type)
    a=a.dropna(subset=['类别'])
    a['工位']=i
    alldata=alldata.append(a,ignore_index=True,sort=False)
alldata['更换率']=[(rate_['rp1'])[x] for x in alldata['类别']]
alldata['备件率']=[(rate_['rs1'])[x] for x in alldata['类别']]
alldata['购买数量']=alldata['数量']*(alldata['更换率']+alldata['备件率'])
def groupbyID(x):
    d = {}
    d['型号'] = x['型号'].iloc[0]
    d['名称'] = x['名称'].iloc[0]
    d['name'] = x['name'].iloc[0]
    d['OEM'] = x['OEM'].iloc[0]
    d['备注'] = (x['工位'].apply(str)+' '+x['备注'].apply(str)+' '+x['数量'].apply(str)+'个').str.cat(sep=';/')
    d['总数量']=x['数量'].sum()
    d['购买总数'] = x['购买数量'].sum()
    return pd.Series(d, index=['型号','名称','name','OEM','备注','总数量','购买总数'])

partdata=alldata.groupby('订货号').apply(groupbyID)
partdata.to_excel('partdata.xlsx')
alldata.to_excel('alldata.xlsx')
