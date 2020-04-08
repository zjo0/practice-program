import pandas as pd
import numpy as np
from sklearn import linear_model
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
a=pd.read_excel('D:\project\GF9 P3 VB SLB\项目管理\烟台大面异常\结果数据\data_in.xlsx')
x=np.array(a['位置x'])
y=np.array(a['位置y'])
z=np.array(a['测量值'])
model=linear_model.LinearRegression()
data=np.vstack((x,y)).T
model.fit(data,z)
a['平面值']=model.predict(data)
a['偏离值']=a['测量值']-a['平面值']
predict=np.array(a['偏离值'])
a.to_excel('D:\project\GF9 P3 VB SLB\项目管理\烟台大面异常\结果数据\data_out.xlsx')
fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')
for i in range(len(x)):
    if predict[i]>0:
        ax.plot([x[i],x[i]],[y[i],y[i]],[predict[i],0],color='b',marker='s')
    else:
        ax.plot([x[i],x[i]],[y[i],y[i]],[predict[i],0],color='r',marker='s')
plt.xlabel('x')
plt.ylabel('y')
xplot=np.linspace(min(x),max(x),3)
yplot=np.linspace(min(y),max(y),3)
xplot,yplot=np.meshgrid(xplot,yplot)
zplot=np.zeros((3,3))
ax.plot_surface(xplot,yplot,zplot, rstride=1, cstride=1, cmap=plt.cm.hot,alpha=0.4)
plt.show()
