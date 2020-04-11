import pandas as pd
import numpy as np
from sklearn import linear_model
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


def draw(path=None):
    if not path:
        messagebox.showerror('路径错误', '请输入数据路径')
    else:
        try:
            a = pd.read_excel(path)
            x = np.array(a['位置x'])
            y = np.array(a['位置y'])
            z = np.array(a['测量值'])
            name = list(a['点号'])
        except:
            messagebox.showerror('文件格式错误', '请按模板格式输入数据')
        else:
            if a.isnull().values.any():
                messagebox.showerror('文件格式错误', '点号，位置，测量值数量不相等')
            else:
                a=a.loc[:,['点号','位置x','位置y','测量值']]
                model = linear_model.LinearRegression()
                data = np.vstack((x, y)).T
                model.fit(data, z)
                a['平面值'] = model.predict(data)
                a['偏离值'] = a['测量值'] - a['平面值']
                error = np.array(a['偏离值'])
                predict = np.array(a['平面值'])
                a.to_excel('data_out.xlsx',index=False)
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                for i in range(len(x)):
                    if error[i] > 0:
                        ax.plot([x[i], x[i]], [y[i], y[i]], [z[i], predict[i]], 'b--', marker='s')
                    else:
                        ax.plot([x[i], x[i]], [y[i], y[i]], [z[i], predict[i]], 'r--', marker='s')
                    ax.text(x[i], y[i], z[i], '{:}:{:.2}'.format(name[i], error[i]))
                plt.xlabel('x')
                plt.ylabel('y')
                xplotraw = np.linspace(min(x), max(x), 2)
                yplotraw = np.linspace(min(y), max(y), 2)
                xplot, yplot = np.meshgrid(xplotraw, yplotraw)
                zplotraw = np.hstack((xplot.reshape(-1, 1), yplot.reshape(-1, 1)))
                zplot = model.predict(zplotraw).reshape(2, 2)
                ax.plot_surface(xplot, yplot, zplot, rstride=1, cstride=1, cmap=plt.cm.hot, alpha=0.4)
                plt.show()






def tample():
    a = pd.DataFrame(columns=['点号','位置x', '位置y', '测量值'])
    a.to_excel('data_in.xlsx',index=False)


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.path = StringVar()
        self.createWidgets()

    def createWidgets(self):
        self.pathlabel = Label(self, text='数据路径').grid(row=0, column=0)
        self.entry = Entry(self, textvariable=self.path).grid(row=0, column=1)
        self.selectButton = Button(self, text='路径选择', command=self.select_path).grid(row=0, column=2)
        self.createButton = Button(self, text='生成模板文件', command=tample).grid(row=1, column=0)
        self.createButton = Button(self, text='平面偏移分析', command=lambda: draw(self.path.get())).grid(row=1, column=1)

    def select_path(self):
        path1_ = filedialog.askopenfilename()
        path1_ = path1_.replace('/', '\\\\')
        self.path.set(path1_)


app = Application()
app.master.title('平面度评价')
app.mainloop()
