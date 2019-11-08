import numpy as np
import pandas as pd
officepath=input('办公室打卡文件带路径,类似\nD:\Desktop\考勤记录表20191031-上海公司.xls\n')
office_original=pd.read_excel(officepath)
office_original['日期']=pd.to_datetime(office_original['日期'])#convert type from str to datetime
dingdingpath=input('钉钉打卡文件带路径,类似\nD:\Desktop\钉钉签到报表(上海业务平台).xls\n')
dingding_original=pd.read_excel(dingdingpath,header=2)#header=2 to ignore first two row
dingding_original['日期']=pd.to_datetime(dingding_original['日期'])
office_record=office_original.set_index(['姓名','日期']).loc[:,['上班签到时间','下班签退时间']].rename({'上班签到时间':'单位签到时间', '下班签退时间':'单位签退时间'},axis='columns')#set multiindex and rename them
dingding_sort=dingding_original.set_index(['姓名','日期']).rename({'aBian':'卞庆荣'})
dingding_onrecord=dingding_sort.groupby(['姓名','日期']).min().loc[:,['地点','时间']].rename({'地点':'钉钉上班地','时间':'钉钉上班时间'},axis='columns')#select the last item for each day as the last record time
dingding_offrecord=dingding_sort.groupby(['姓名','日期']).max().loc[:,['地点','时间']].rename({'地点':'钉钉下班地','时间':'钉钉下班时间'},axis='columns')#select the first item for each day as the last record time
dayoffrecordpath=input('请假记录,类似\nD:Desktop\dataset.xls\n')
dayoffrecord_original=pd.read_excel(dayoffrecordpath,header=1)
dayoffrecord=pd.DataFrame(columns=['姓名','日期','是否请假']).set_index('日期')
def huizong(a):
    b=pd.DataFrame(index=pd.Index(pd.date_range(a['开始时间'],a['结束时间'],freq='D'),name='日期'))
    b['姓名']=a['员工姓名']
    b['是否请假']=True
    global dayoffrecord
    dayoffrecord=dayoffrecord.append(b)
dayoffrecord_original.apply(huizong,axis=1)#work off start date and end date are listed in the same row in the original data
dayoffrecord=dayoffrecord.set_index(['姓名',dayoffrecord.index]).sort_values(['姓名','日期'])
union_record=office_record.copy()
union_record=union_record.reindex(union_record.index.union(dayoffrecord.index).union(dingding_onrecord.index).union(dingding_offrecord.index))#three DataFrame index united
union_record=union_record.join(dingding_onrecord).join(dingding_offrecord).join(dayoffrecord)#three DataFrame united
union_record['是否正常']='异常'
def detect(a):
    a1=a2=0
    if(a['单位签到时间']==a['单位签到时间']):
        if(a['单位签到时间']<'09:30:00'):
            a1=1
    if (a['钉钉上班时间'] == a['钉钉上班时间']):
        if(a['钉钉上班时间'] < '09:30:00'):
            a1 = 1
    if (a['单位签退时间'] == a['单位签退时间']):
        if (a['单位签退时间'] > '18:00:00'):
            a2 = 1
    if (a['钉钉下班时间'] == a['钉钉下班时间']):
        if (a['钉钉下班时间'] > '18:00:00'):
            a2 = 1
    if(a1+a2==2):
        a['是否正常'] = '正常'
    if(a['是否请假']==True):
        a['是否正常'] = '正常'
    return a
union_record.apply(detect,axis=1)#determine whether one person record has issue for each day
union_record.to_excel('union.xlsx')
print('work done')