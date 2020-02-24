import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
a=pd.read_excel('测量数据.xlsx')
a['测量偏差']=abs(a['测量']-a['复测'])
error=a.sort_values(by='测量偏差')['测量偏差'].iloc[-2]
Dm=error*(2**0.5)
a['香肠大值']=(a['测量']+a['复测'])/2+Dm/2/(2**0.5)-(Dm**2/4-(a['测量']-a['复测'])**2/2)**0.5/(2**0.5)
a['香肠小值']=(a['测量']+a['复测'])/2-Dm/2/(2**0.5)+(Dm**2/4-(a['测量']-a['复测'])**2/2)**0.5/(2**0.5)
a1=a['香肠大值'].max()
a2=a['香肠小值'].min()
Dp=a1-a2
plt.scatter(a['测量'],a['复测'])
axismax=1.2*max(a['测量'].max(),a['复测'].max())
plt.axis([0,axismax,0,axismax],'scaled')
plt.plot([0,axismax],[0,axismax],'k--')
theta1=np.arange(-0.25*np.pi,0.75*np.pi,0.01)
theta2=np.arange(0.75*np.pi,1.75*np.pi,0.01)
x1=a1-error/2+Dm/2*np.cos(theta1)
y1=a1-error/2+Dm/2*np.sin(theta1)
x2=a2+error/2+Dm/2*np.cos(theta2)
y2=a2+error/2+Dm/2*np.sin(theta2)
plt.plot(x1,y1,'b-')
plt.plot(x2,y2,'b-')
plt.plot([a1-error,a2],[a1,a2+error],'b-')
plt.plot([a2+error,a1],[a2,a1-error],'b-')
plt.text(0.5,axismax*0.8,'△m=%.3f,△p=%.3f,DR=%.2f'%(Dm,Dp,Dp/Dm))
plt.show()
