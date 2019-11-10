from tkinter import *
from tkinter import filedialog
from 考勤 import unionrecord

class Application(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.pack()
        self.officepath=StringVar()   
        self.dingdingpath=StringVar()
        self.workoffpath=StringVar()
        self.createWidgets()
    def createWidgets(self):
        self.officeLabel=Label(self,text='办公室打卡文件路径').grid(row=0,column=0)
        self.entry=Entry(self, textvariable=self.officepath).grid(row=0, column=1)
        self.selectButton1=Button(self,text='路径选择',command=self.select_office_path).grid(row=0,column=2)
        self.dingdingLabel = Label(self, text='钉钉打卡文件路径').grid(row=1, column=0)
        self.entry = Entry(self, textvariable=self.dingdingpath).grid(row=1, column=1)
        self.selectButton2 = Button(self, text='路径选择', command=self.select_dingding_path).grid(row=1, column=2)
        self.workoffLabel = Label(self, text='请假文件路径').grid(row=2, column=0)
        self.entry = Entry(self, textvariable=self.workoffpath).grid(row=2, column=1)
        self.selectButton3 = Button(self, text='路径选择', command=self.select_workoff_path).grid(row=2, column=2)
        self.createButton=Button(self,text='生成汇总文件',command=lambda : unionrecord(self.officepath.get(),self.dingdingpath.get(),self.workoffpath.get())).grid(row=3)
    def select_office_path(self):
        path1_=filedialog.askopenfilename()
        path1_=path1_.replace('/','\\\\')
        self.officepath.set(path1_)
    def select_dingding_path(self):
        path2_=filedialog.askopenfilename()
        path2_=path2_.replace('/','\\\\')
        self.dingdingpath.set(path2_)
    def select_workoff_path(self):
        path3_=filedialog.askopenfilename()
        path3_=path3_.replace('/','\\\\')
        self.workoffpath.set(path3_)
app=Application()
app.master.title('感谢健哥')
app.mainloop()