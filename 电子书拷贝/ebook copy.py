#需要打开电子书，才能截屏
import pyautogui as gui
a=int(input('一共几页书'))
gui.run('g500,0 l')
for i in range(a):
    b='%s.png'%i
    gui.screenshot(b)
    gui.run("k'down'")
    
    
    
