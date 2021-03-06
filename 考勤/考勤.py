import numpy as np
import pandas as pd
import calendar
def unionrecord(officepath, dingdingpath, dayoffrecordpath,dingdingonpath,year_,month_):
    wholedate=pd.date_range('%s-%s-01'%(year_,month_),periods=calendar.monthrange(year_,month_)[1])
    try:
        office_original = pd.read_excel(officepath)
        office_original['日期'] = pd.to_datetime(office_original['日期'])  # convert type from str to datetime
        office_record = office_original.set_index(['姓名', '日期']).loc[:, ['上班签到时间', '下班签退时间']].rename({'上班签到时间': '单位签到时间', '下班签退时间': '单位签退时间'}, axis='columns')  # set multiindex and rename them
    except:
        print('办公室打卡记录提取失败')
        office_record=pd.DataFrame(columns=['姓名','日期','单位签到时间','单位签退时间']).set_index(['姓名','日期'])#读取办公室打卡记录失败后，建立空文件
    try:
        dingding_original = pd.read_excel(dingdingpath, header=2)  # header=2 to ignore first two row
        dingding_original['日期'] = pd.to_datetime(dingding_original['日期'])
        dingding_sort = dingding_original.set_index(['姓名', '日期']).rename({'aBian': '卞庆荣','李珺琪 yuki':'李珺琪'})
        def onoffice(x):
            x=x.sort_values(by='时间')
            d={}
            d['钉钉上班地']=x['地点'].iloc[0]
            d['钉钉上班时间']=x['时间'].iloc[0]
            return pd.Series(d,index=['钉钉上班地','钉钉上班时间'])
        def offoffice(x):
            x=x.sort_values(by='时间')
            d={}
            d['钉钉下班地']=x['地点'].iloc[-1]
            d['钉钉下班时间']=x['时间'].iloc[-1]
            return pd.Series(d,index=['钉钉下班地','钉钉下班时间'])
        dingding_onrecord = dingding_sort.groupby(['姓名', '日期']).apply(onoffice) # select the last item for each day as the last record time
        dingding_offrecord = dingding_sort.groupby(['姓名', '日期']).apply(offoffice)  # select the first item for each day as the last record time
    except:
        print('钉钉打卡记录读取失败')
        dingding_onrecord = pd.DataFrame(columns=['姓名','日期','钉钉上班地','钉钉上班时间']).set_index(['姓名','日期'])#读取钉钉打卡记录失败后，建立空文件
        dingding_offrecord = pd.DataFrame(columns=['姓名','日期','钉钉下班地','钉钉下班时间']).set_index(['姓名','日期'])#读取钉钉打卡记录失败后，建立空文件
    

    def huizong(a,dayoffrecord_):
        startday,starthalf=a['请假开始时间'].split(' ')
        endday,endhalf=a['请假结束时间'].split(' ')
        b = pd.DataFrame(index=pd.Index(pd.date_range(startday, endday, freq='D'), name='日期'),columns=['姓名','上午请假','下午请假'])
        b['姓名'] = a['员工姓名']
        b['上午请假'] = True
        b['下午请假']= True
        if starthalf=="下午":
            b.iloc[0,1]=False
        if endhalf=="上午":
            b.iloc[-1,2]=False
        dayoffrecord_[0] = dayoffrecord_[0].append(b)

    try:
        dayoffrecord_original = pd.read_excel(dayoffrecordpath, header=0)
        dayoffrecord_ = [pd.DataFrame(columns=['姓名', '日期', '上午请假','下午请假']).set_index('日期')]
        dayoffrecord_original.apply(lambda x:huizong(x,dayoffrecord_),axis=1)  # work off start date and end date are listed in the same row in the original data
        dayoffrecord = dayoffrecord_[0]
        dayoffrecord = dayoffrecord.set_index(['姓名', dayoffrecord.index]).sort_values(['姓名', '日期'])
    except:
        print('请假记录读取失败')
        dayoffrecord =pd.DataFrame(columns=['姓名','日期','上午请假','下午请假']).set_index(['姓名','日期'])#读取请假记录失败后，建立空文件
    try:
        dingdingworkon_original=pd.read_excel(dingdingonpath,sheet_name='每日统计',header=2)
        dingdingworkon_original=dingdingworkon_original.drop([0])
        def datedropweek(a):
            a['日期']=str(a['日期']).split(' ')[0]
            return a
        dingdingworkon_record=dingdingworkon_original.apply(datedropweek,axis=1)
        dingdingworkon_record['日期']=pd.to_datetime(dingdingworkon_record['日期'],format='%y-%m-%d')
        dingdingworkon_record=dingdingworkon_record.set_index(['姓名', '日期']).loc[:, ['上班1', '下班1']].rename({'上班1': '钉钉上班考勤', '下班1': '钉钉下班考勤'},axis='columns')
    except:
        print('钉钉考勤读取失败')
        dingdingworkon_record=pd.DataFrame(columns=['姓名','日期','钉钉上班考勤','钉钉下班考勤']).set_index(['姓名','日期'])#读取请假记录失败后，建立空文件
    union_record = office_record.copy()
    union_record = union_record.reindex(union_record.index.union(dayoffrecord.index).union(dingding_onrecord.index).union(dingding_offrecord.index).union(dingdingworkon_record.index))  # three DataFrame index united
    wholeindex=pd.MultiIndex.from_product([union_record.index.get_level_values(0).drop_duplicates(),wholedate],names=['姓名','日期'])#读取三个文件中提到的所有姓名，与本月所有的日期组成MultiIndex
    union_record=union_record.reindex(union_record.index.union(wholeindex))
    union_record = union_record.join(dingding_onrecord).join(dingding_offrecord).join(dayoffrecord).join(dingdingworkon_record)  # three DataFrame united
    union_record['是否正常'] = '异常'


    def detect(a):
        a1 = a2 = a11=a21=0
        morningoff=afternoonoff=False
        if a['上午请假']==True:
            morningoff=True
        if a['下午请假']==True:
            afternoonoff=True

        if (a['单位签到时间'] == a['单位签到时间']):
            if (a['单位签到时间'] < '09:30:00'):
                a1 = 1
            if (a['单位签到时间'] < '13:00:00'):
                a11 = 1
            if (a['单位签到时间'] < '06:00:00'):
                a1 = 3
        if (a['钉钉上班时间'] == a['钉钉上班时间']):
            if (a['钉钉上班时间'] < '09:30:00'):
                a1 = 1
            if (a['钉钉上班时间'] < '13:00:00'):
                a11 = 1
            if (a['钉钉上班时间'] < '06:00:00'):
                a1 = 3
        if (a['钉钉上班考勤'] == a['钉钉上班考勤']):
            if (a['钉钉上班考勤'] < '09:30:00'):
                a1 = 1
            if (a['钉钉上班考勤'] < '13:00:00'):
                a11 = 1
            if (a['钉钉上班考勤'] < '06:00:00'):
                a1 = 3
        if morningoff==True:
            if a11==1:
                a1=1
        if (a['单位签退时间'] == a['单位签退时间']):
            if (a['单位签退时间'] > '18:00:00'):
                a2 = 1
            if (a['单位签退时间'] > '12:00:00'):
                a21 = 1
        if (a['钉钉下班时间'] == a['钉钉下班时间']):
            if (a['钉钉下班时间'] > '18:00:00'):
                a2 = 1
            if (a['钉钉下班时间'] > '12:00:00'):
                a21 = 1
        if (a['钉钉下班考勤'] == a['钉钉下班考勤']):
            if (a['钉钉下班考勤'] > '18:00:00'):
                a2 = 1
            if (a['钉钉下班考勤'] > '12:00:00'):
                a21 = 1
        if afternoonoff==True:
            if a21==1:
                a2=1
        if (a1 + a2 == 2):
            a['是否正常'] = '正常'
        if (morningoff == True & afternoonoff==True):
            a['是否正常'] = '正常'
        if (a1==3):
            a['是否正常']='凌晨有打卡'
        return a

    union_record.apply(detect, axis=1)  # determine whether one person record has issue for each day
    union_record.loc[union_record.index.get_level_values(1).weekday>4,'是否正常'] ='周末'
    union_record=union_record.rename({'单位签到时间': '指纹上班时间', '单位签退时间': '指纹下班时间', '钉钉上班地': '钉钉签到上班地点', '钉钉上班时间': '钉钉签到上班时间', '钉钉下班地': '钉钉签到上班地点', '钉钉下班时间': '钉钉签到下班时间', '钉钉上班考勤': '钉钉考勤上班时间', '钉钉下班考勤': '钉钉考勤下班时间'}, axis='columns')
    union_record.to_excel('union.xlsx')
    print('work done')

if __name__ == '__main__':
    officepath = input('办公室打卡文件带路径,类似\nD:\Desktop\考勤记录表20191031-上海公司.xls\n')
    dingdingpath = input('钉钉打卡文件带路径,类似\nD:\Desktop\钉钉签到报表(上海业务平台).xls\n')
    dayoffrecordpath = input('请假记录,类似\nD:Desktop\dataset.xls\n')
    dingdingonpath = input('钉钉考勤记录,类似\nD:Desktop\dataset.xls\n')
    unionrecord(officepath,dingdingpath,dayoffrecordpath,dingdingonpath)


