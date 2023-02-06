import os
import shutil
import webbrowser
import threading
import requests
import re
from tkinter import *
from ttkbootstrap import Combobox
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
"""我知道有更好的写法但是以我的水平就只能写成这样了"""

#   打包点位功能
def pack_json_data():
    try:
        data_path = filedialog.askdirectory(title='选择需要打包的文件夹', initialdir=cheat_path)
        data_name = filedialog.asksaveasfilename(title='选择保存位置并重命名文件', initialfile='请为点位文件命名',
                                                 initialdir=cheat_path)
        shutil.make_archive(data_name, 'zip', data_path)
    except Exception:
        pass


#   上传点位文件到服务器
def upload_json_data():
    webbrowser.open('http://162.14.77.126:4567')


#   清空点位功能
def clear():
    try:
        if os.path.exists(f'{cheat_path}/teleports'):
            shutil.rmtree(f'{cheat_path}/teleports')
            os.mkdir(f'{cheat_path}/teleports')
            messagebox.showinfo(title='提示', message='清空完毕')
    except Exception:
        messagebox.showerror(title='提示', message='清空失败')


#   检查更新
def check_update():
    resp = requests.get('http://www.pyforme.fun/update.html').text
    if resp != '1.02':
        messagebox.showinfo(title='提示', message='当前有可用版本更新')
        webbrowser.open('http://www.pyforme.fun/update/point_switch.exe')
    else:
        messagebox.showinfo(title='提示', message='当前已是最新版本')


#   解压从服务器下载好的点位文件
def unpack_json_data():
    shutil.unpack_archive(f'./data.zip', f'{cheat_path}/teleports')


#   多线程防止运行时卡死
def thread(func):
    t = threading.Thread(target=func)
    t.start()


#   获取神瞳类的页面
def get_oculus():
    list_box.delete(first=0, last=END)
    resp = requests.get('http://www.pyforme.fun/oculus/oculus.html')
    resp.encoding = 'utf-8'
    title = re.findall(r'<li>(.*?)</li>', resp.text)
    for _ in title:
        list_box.insert(END, _)


#   获取宝箱类的页面
def get_chests():
    list_box.delete(first=0, last=END)
    resp = requests.get('http://www.pyforme.fun/chests/chests.html')
    resp.encoding = 'utf-8'
    title = re.findall(r'<li>(.*?)</li>', resp.text)
    for _ in title:
        list_box.insert(END, _)


#   获取材料类的页面
def get_items():
    list_box.delete(first=0, last=END)
    resp = requests.get('http://www.pyforme.fun/items/items.html')
    resp.encoding = 'utf-8'
    title = re.findall(r'<li>(.*?)</li>', resp.text)
    for _ in title:
        list_box.insert(END, _)


#   获取掉落物类的页面
def get_loots():
    list_box.delete(first=0, last=END)
    resp = requests.get('http://www.pyforme.fun/loots/loots.html')
    resp.encoding = 'utf-8'
    title = re.findall(r'<li>(.*?)</li>', resp.text)
    for _ in title:
        list_box.insert(END, _)


#   获取锚点类的页面
def get_teleports():
    list_box.delete(first=0, last=END)
    resp = requests.get('http://www.pyforme.fun/teleports/teleports.html')
    resp.encoding = 'utf-8'
    title = re.findall(r'<li>(.*?)</li>', resp.text)
    for _ in title:
        list_box.insert(END, _)


#   通过改变title部分来下载对应的点位文件
def change_point():
    try:
        title = list_box.selection_get()
        if title != '':
            resp = requests.get(f'http://www.pyforme.fun:3333/{title}.zip').content
            open(f'./data.zip', 'wb').write(resp)
            if os.path.exists(f'{cheat_path}/teleports'):
                shutil.rmtree(f'{cheat_path}/teleports')
            unpack_json_data()
            os.remove('./data.zip')
            messagebox.showinfo(title='提示', message=f'点位"{title}"切换成功')
    except Exception:
        messagebox.showwarning(title='提示', message='请选择一个点位')
        if os.path.exists('./data.zip'):
            os.remove('./data.zip')


#   通过对文件夹的更改名称和dll文件的删除，解压依赖包来实现转服功能
def change_game_type():
    try:
        if not os.path.exists('./game_path.ini'):
            set_game_path = filedialog.askdirectory(title='请选择Genshin Impact Game文件夹')  # 选择游戏目录并生成路径文件
            open('./game_path.ini', 'w', encoding='utf-8').write(set_game_path)
        game = game_type.selection_get()
        game_path = open('./game_path.ini', 'r', encoding='utf-8').read()
        if game_path == '':
            os.remove('./game_path.ini')
            messagebox.showwarning(title='警告', message='请选择正确的路径')
            change_game_type()
        if os.path.exists(f'{game_path}/YuanShen_Data/Plugins/metakeeper.dll'):  # 通过判断不同的文件是否存在来判断当前服务器类型
            gt.set(value='当前为：官服')
            open('./game_type.ini', 'w', encoding='utf-8').write('官服')
        elif os.path.exists(f'{game_path}/YuanShen_Data/Plugins/PCGameSDK.dll'):
            gt.set(value='当前为：b服')
            open('./game_type.ini', 'w', encoding='utf-8').write('b服')
        elif os.path.exists(f'{game_path}/GenshinImpact.exe') and os.path.exists(f'{game_path}/GenshinImpact_Data'):
            gt.set(value='当前为：国际服')
            open('./game_type.ini', 'w', encoding='utf-8').write('国际服')
        if game == '官服转b服':
            if not os.path.exists('./data/game_pack/官转b.zip'):
                if messagebox.askyesno(title='提示', message='未检测到官转b资源包，是否前往下载?'):
                    webbrowser.open('http://www.pyforme.fun/packs/官转b.zip')
            else:
                shutil.unpack_archive('./data/game_pack/官转b.zip', f'{game_path}')
                os.remove(f'{game_path}/YuanShen_Data/Plugins/metakeeper.dll')
                gt.set(value='当前为：b服')
                open('./game_type.ini', 'w', encoding='utf-8').write('b服')
                messagebox.showinfo(title='提示', message='已从官服切换为b服')
        elif game == 'b服转官服':
            if not os.path.exists('./data/game_pack/b转官.zip'):
                if messagebox.askyesno(title='提示', message='未检测到b转官资源包，是否前往下载?'):
                    webbrowser.open('http://www.pyforme.fun/packs/b转官.zip')
            else:
                shutil.unpack_archive('./data/game_pack/b转官.zip', f'{game_path}')
                os.remove(f'{game_path}/YuanShen_Data/Plugins/PCGameSDK.dll')
                gt.set(value='当前为：官服')
                open('./game_type.ini', 'w', encoding='utf-8').write('官服')
                messagebox.showinfo(title='提示', message='已从b服切换为官服')
        elif game == '官服转国际服':
            if not os.path.exists('./data/game_pack/官转国.zip'):
                if messagebox.askyesno(title='提示', message='未检测到官转国资源包，是否前往下载?'):
                    webbrowser.open('http://www.pyforme.fun/packs/官转国.zip')
            else:
                os.rename(f'{game_path}/YuanShen_Data', f'{game_path}/GenshinImpact_Data')
                os.remove(f'{game_path}/YuanShen.exe')
                shutil.unpack_archive('./data/game_pack/官转国.zip', f'{game_path}')
                gt.set(value='当前为：国际服')
                open('./game_type.ini', 'w', encoding='utf-8').write('国际服')
                messagebox.showinfo(title='提示', message='已从官服切换为国际服')
        elif game == '国际服转官服':
            if not os.path.exists('./data/game_pack/国转官.zip'):
                if messagebox.askyesno(title='提示', message='未检测到国转官资源包，是否前往下载?'):
                    webbrowser.open('http://www.pyforme.fun/packs/国转官.zip')
            else:
                os.rename(f'{game_path}/GenshinImpact_Data', f'{game_path}/YuanShen_Data')
                os.remove(f'{game_path}/GenshinImpact.exe')
                shutil.unpack_archive('./data/game_pack/国转官.zip', f'{game_path}')
                gt.set(value='当前为：官服')
                open('./game_type.ini', 'w', encoding='utf-8').write('官服')
                messagebox.showinfo(title='提示', message='已从国际服切换为官服')
        else:
            messagebox.showinfo(title='提示', message='请选择一种转换形式')
    except Exception:
        messagebox.showwarning(title='提示', message='转换失败')


#   没有检测到目录下的cheat_path文件时，需要重新设置并生成路径文件
def first_start():
    if not os.path.exists('./cheat_path.ini'):
        root = Tk()
        root.iconbitmap(default='./data/resources/title.ico')
        set_cheat_path = filedialog.askdirectory(title='请选择Akebi/Acrepi所在目录', mustexist=True)
        if 'teleports' in set_cheat_path:
            set_cheat_path = set_cheat_path.replace('teleports', '')
        if set_cheat_path != '':
            open('./cheat_path.ini', 'w', encoding='utf-8').write(set_cheat_path)
            Tk.destroy(root)
        else:
            messagebox.showwarning(title='警告', message='请选择正确的路径')
            Tk.destroy(root)
            first_start()


first_start()
#   以下为ui布局及按钮功能绑定
window = Tk()
window.geometry('380x420+550+200')
window.title('点位切换器v1.0.2')
window.iconbitmap(default='./data/resources/title.ico')
background = Image.open('./data/resources/background.png')
background_photo = ImageTk.PhotoImage(background)
bglable = Label(window, image=background_photo)
bglable.place(x=0, y=0)
cheat_path = open('./cheat_path.ini', 'r', encoding='utf-8').read()
file_menu = Menu(window)
file_menu.add_command(label='打包点位文件', command=lambda: thread(pack_json_data))
file_menu.add_command(label='上传点位文件', command=lambda: thread(upload_json_data))
file_menu.add_command(label='清空点位文件夹', command=lambda: thread(clear))
file_menu.add_command(label='检查版本更新', command=lambda: thread(check_update))
oculus = Button(window, text='神瞳类', font=('黑体', 18), command=lambda: thread(get_oculus))
oculus.place(x=20, y=20)
chests = Button(window, text='宝箱类', font=('黑体', 18), command=lambda: thread(get_chests))
chests.place(x=20, y=80)
items = Button(window, text='材料类', font=('黑体', 18), command=lambda: thread(get_items))
items.place(x=20, y=140)
loots = Button(window, text='掉落物', font=('黑体', 18), command=lambda: thread(get_loots))
loots.place(x=20, y=200)
teleports = Button(window, text='锚点类', font=('黑体', 18), command=lambda: thread(get_teleports))
teleports.place(x=20, y=260)
gt = StringVar(window, value='当前为:', name='gtype')
game_type = Label(window, textvariable=gt, font=('黑体', 18), bg='blue')
game_type.place(x=20, y=320)
if os.path.exists('./game_type.ini'):
    gt.set(value=f"当前为：{open('./game_type.ini', 'r', encoding='utf-8').read()}")
change_point_bt = Button(window, text='换点', font=('黑体', 14), width=6, command=lambda: thread(change_point))
change_point_bt.place(x=215, y=260)
game_type = Combobox(window, width=16, values=('官服转b服', 'b服转官服', '官服转国际服', '国际服转官服'),
                     state='readonly', font='黑体')
game_type.place(x=216, y=210)
change_game_type_bt = Button(window, text='换服', font=('黑体', 14), width=6, command=lambda: thread(change_game_type))
change_game_type_bt.place(x=305, y=260)
list_box = Listbox(window, height=9, width=20)
list_box.place(x=220, y=20)
s = Scrollbar(list_box, relief='raised')
list_box.config(yscrollcommand=s.set)
s.config(command=list_box.yview)
s.place(x=124, y=-1, height=164)
window.config(menu=file_menu)
window.mainloop()
