import mysql.connector
config={'host':'127.0.0.1',#默认127.0.0.1
        'user':'root',
        'password':'catalogcreator',
        'port':3356 ,#默认即为3306
        'database':'cc_catalogs',
        'charset':'utf8'#默认即为utf8
        }
try:
    cnn=mysql.connector.connect(**config)
except mysql.connector.Error as e:
    print('connect fails {}'.format(e))
cursor=cnn.cursor()
try:
    sql_query="SELECT p.part_id,p.parent_id,p.link_id,v2.value_0,v4.value_0,v5.value_0,v6.value_2,v6.value_6,v9.value_0 FROM cc_e54421a47341dd712e3ffdc1277f7b1c_tbl_part_properties AS p ,cc_e54421a47341dd712e3ffdc1277f7b1c_tbl_part_values_2 AS v2 ,cc_e54421a47341dd712e3ffdc1277f7b1c_tbl_part_values_4 AS v4 ,cc_e54421a47341dd712e3ffdc1277f7b1c_tbl_part_values_5 AS v5 ,cc_e54421a47341dd712e3ffdc1277f7b1c_tbl_part_values_6 AS v6 ,cc_e54421a47341dd712e3ffdc1277f7b1c_tbl_part_values_9 AS v9 WHERE p.part_id = v2.part_id AND p.part_id = v4.part_id AND p.part_id = v5.part_id AND p.part_id = v6.part_id AND p.part_id = v9.part_id"
    cursor.execute(sql_query)
    searchresult=cursor.fetchall()#得到part id，父装配体id，对应装配体id-1，装配数量，GROB订货号，GROB型号，部件英文名，部件中文名，OEM
finally:
    cursor.close()
    cnn.close()

def collectall(originallist,wantlist):#迭代搜索所有装配子部件清单及数量，originallist是数据库返回初始数据，wantlist是主动输入的希望查找的部件及其所有子装配部件。
    finallist=[]#所有装配部件清单
    firstlist=[]#一级装配体清单
    for j in originallist:
        if j[1] in wantlist:
            firstlist.append(j)
    for i in firstlist:
        appendson(i,1,originallist,finallist)
    return finallist

def appendson(a,n,originallist,finallist):#迭代搜索子部件程序，子部件数量要和上级数量相乘，
    b=list(a)
    b[3]=int(b[3])*n
    finallist.append(b)
    if b[2]!=0:
        for i in originallist:
            if i[1]==(b[2]+1):
                appendson(i,b[3],originallist,finallist)
a=collectall(searchresult,[4063])
print(a)



