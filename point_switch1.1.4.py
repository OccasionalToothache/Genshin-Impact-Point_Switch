import os
import shutil
import sys
import webbrowser
import threading
import requests
import re
import datetime
import configparser
import tkinter as tk
from natsort import natsorted
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog


class PointSwitch:
    def __init__(self, master):
        self.master = master
        self.config = None
        master.title('点位切换器v1.1.4')
        master.geometry('352x340+550+200')
        master.resizable(False, False)
        master.wm_attributes('-topmost', 1)
        master.iconbitmap(default='title.ico')
        self.Menus()
        self.MainUI()
        self.Config()
        self.CheckUpdate()

    def Menus(self):
        self.MainMenu = tk.Menu(self.master)
        self.master.config(menu=self.MainMenu)
        self.AboutMenu = tk.Menu(self.MainMenu, tearoff=0)
        self.MainMenu.add_command(label='打包点位文件', command=lambda: self.Thread(self.PackPoint))
        self.MainMenu.add_command(label='上传点位文件', command=lambda: self.Thread(webbrowser.open(url='http://www.pyforme.fun:4567')))
        self.MainMenu.add_command(label='清空点位文件', command=lambda: self.Thread(self.ClearPoints))
        self.AboutMenu.add_command(label='使用文档', command=lambda: self.Thread(webbrowser.open(url='http://www.pyforme.fun/read/manual.html')))
        self.AboutMenu.add_command(label='检查更新', command=lambda: self.Thread(self.CheckUpdate))
        self.AboutMenu.add_command(label='清除配置', command=lambda: self.Thread(self.ResetConfig))
        self.MainMenu.add_cascade(label='查看更多内容', menu=self.AboutMenu)

    def MainUI(self):
        self.Oculus = tk.Button(master=self.master, text='神瞳类', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('oculus')))
        self.Oculus.place(x=20, y=20)
        self.Chests = tk.Button(master=self.master, text='宝箱类', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('chests')))
        self.Chests.place(x=20, y=80)
        self.Items = tk.Button(master=self.master, text='采集物', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('items')))
        self.Items.place(x=20, y=140)
        self.Monsters = tk.Button(master=self.master, text='怪物类', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('monsters')))
        self.Monsters.place(x=20, y=200)
        self.Auto = tk.Button(master=self.master, text='锄地类', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('auto')))
        self.Auto.place(x=20, y=260)
        self.PointsBox = tk.Listbox(master=self.master, height=9)
        self.Scrollbar = tk.Scrollbar(master=self.master, orient='vertical')
        self.PointsBox.config(yscrollcommand=self.Scrollbar.set)
        self.Scrollbar.config(command=self.PointsBox.yview)
        self.Scrollbar.place(x=307, y=22, height=163)
        self.PointsBox.place(x=180, y=20, width=145)
        self.Gametype = Combobox(master=self.master, width=15, state='readonly',font=('黑体', 12))
        self.Gametype.place(x=181, y=200)
        self.ChangePoint = tk.Button(master=self.master, text='换点', font=('黑体', 14),command=lambda: self.Thread(self.PointChange))
        self.ChangePoint.place(x=180, y=240)
        self.ChangeGametype = tk.Button(master=self.master, text='换服', font=('黑体', 14), command=lambda: self.Thread(self.GameTypeChange))
        self.ChangeGametype.place(x=270, y=240)

    def Thread(self, func):
        threading.Thread(target=func).start()

    def PackPoint(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        cheatpath = config['DEFAULT']['cheatpath']
        pointpath = filedialog.askdirectory(title='请选择需要打包的文件路径', initialdir=cheatpath)
        if pointpath:
            pointname = filedialog.asksaveasfilename(title='请选择文件保存的路径', initialfile=datetime.datetime.now().strftime('%H%M%S'), initialdir=cheatpath)
            if pointname:
                shutil.make_archive(pointname, 'zip', pointpath)
                messagebox.showinfo(title='提示', message=f'点位文件已成功打包到{pointname}')

    def ClearPoints(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        cheatpath = self.config['DEFAULT']['cheatpath']
        if not os.path.exists(f'{cheatpath}/teleports'):
            os.mkdir(f'{cheatpath}/teleports')
        else:
            shutil.rmtree(f'{cheatpath}/teleports')
            os.mkdir(f'{cheatpath}/teleports')
        messagebox.showinfo(title='提示', message='点位文件夹已清空')

    def CheckUpdate(self):
        response = requests.get(url='http://www.pyforme.fun/update.html').text
        if response != '1.1.4':
            if messagebox.askyesno(title='更新', message='检测到最新版本，是否更新'):
                webbrowser.open(url='http://www.pyforme.fun/update/Pointswitch_Setup.exe')
                sys.exit()
            else:
                sys.exit()
        else:
            self.config = configparser.ConfigParser()
            self.config.read('config.ini')
            if self.config['DEFAULT']['showupdate'] == 'enable':
                messagebox.showinfo(title='更新', message='当前已是最新版本')
            else:
                self.config.set('DEFAULT', 'showupdate', 'enable')
                with open('config.ini', 'w') as configfile:
                    self.config.write(configfile)

    def GetPoints(self, type):
        self.type = type
        response = requests.get(url=f'http://www.pyforme.fun/{self.type}/{self.type}.html')
        response.encoding = 'utf-8'
        PointList = re.findall(r'<li>(.*?)</li>', response.text)
        self.PointsBox.delete(first=0, last=tk.END)
        for Points in PointList:
            self.PointsBox.insert(tk.END, Points)

    def PointChange(self):
        Selection = self.PointsBox.curselection()
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        if Selection:
            response = requests.get(url=f'http://www.pyforme.fun:3333/{self.PointsBox.get(Selection[0])}.zip').content
            open('data.zip', 'wb').write(response)
            if os.path.exists(f'{self.config["DEFAULT"]["cheatpath"]}/teleports'):
                shutil.rmtree(f'{self.config["DEFAULT"]["cheatpath"]}/teleports')
            shutil.unpack_archive(filename='data.zip', extract_dir=f'{self.config["DEFAULT"]["cheatpath"]}/teleports')
            os.remove('data.zip')
            folder_path = f'{self.config["DEFAULT"]["cheatpath"]}/teleports'
            file_names = os.listdir(folder_path)
            json_file_names = natsorted([f for f in file_names if f.endswith('.json')])
            for i, json_file_name in enumerate(json_file_names):
                new_json_file_name = '{:04d}.json'.format(i + 1)
                os.rename(os.path.join(folder_path, json_file_name), os.path.join(folder_path, new_json_file_name))
            messagebox.showinfo(title='提示', message=f'点位{self.PointsBox.get(Selection[0])}切换成功')
        else:
            messagebox.showwarning(title='提示', message='请选择一个点位')

    def GameTypeChange(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        gamepath = self.config['DEFAULT']['gamepath']
        Value = self.Gametype.get()
        if Value == '官服转b服':
            shutil.unpack_archive(filename='./data/官转b.zip', extract_dir=gamepath)
            os.remove(f'{gamepath}/YuanShen_Data/Plugins/metakeeper.dll')
            messagebox.showinfo(title='提示', message='已成功从官服转为b服')
        elif Value == 'b服转官服':
            shutil.unpack_archive(filename='./data/b转官.zip', extract_dir=gamepath)
            os.remove(f'{gamepath}/YuanShen_Data/Plugins/PCGameSDK.dll')
            messagebox.showinfo(title='提示', message='已成功从b服转为官服')
        elif Value == '官服转国际服':
            if not os.path.exists('./data/官转国3.4.zip'):
                if messagebox.askyesno(title='提示', message='未检测到官转国依赖包，是否前往下载'):
                    webbrowser.open(url='https://pan.baidu.com/s/1w1LYakMPpyuIAv5MWCJDrA?pwd=si1t')
            else:
                os.rename(f'{gamepath}/YuanShen_Data', f'{gamepath}/GenshinImpact_Data')
                os.remove(f'{gamepath}/YuanShen.exe')
                shutil.unpack_archive(filename='./data/官转国3.4.zip', extract_dir=gamepath)
                messagebox.showinfo(title='提示', message='已成功从官服转为国际服')
        elif Value == '国际服转官服':
            if not os.path.exists('./data/国转官3.4.zip'):
                if messagebox.askyesno(title='提示', message='未检测到国转官依赖包，是否前往下载'):
                    webbrowser.open(url='https://pan.baidu.com/s/1w1LYakMPpyuIAv5MWCJDrA?pwd=si1t')
            else:
                os.rename(f'{gamepath}/GenshinImpact_Data', f'{gamepath}/YuanShen_Data')
                os.remove(f'{gamepath}/GenshinImpact.exe')
                shutil.unpack_archive(filename='./data/国转官3.4.zip', extract_dir=gamepath)
                messagebox.showinfo(title='提示', message='已成功从国际服转为官服')
        else:
            messagebox.showwarning(title='提示', message='请选择一个选项')
        self.Config()

    def Config(self):
        self.config = configparser.ConfigParser()
        gameconfig = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            self.config.set('DEFAULT', 'cheatpath', filedialog.askdirectory(title='选择点位需要放置的目录'))
            self.config.set('DEFAULT', 'gamepath',filedialog.askdirectory(title='选择Genshin Impact Game文件夹所在目录'))
            self.config.set('DEFAULT', 'showupdate', 'disable')
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
            self.config.read('config.ini')
            if not self.config.has_option('DEFAULT', 'cheatpath') or not self.config.get('DEFAULT', 'cheatpath'):
                messagebox.showwarning(title='提示', message='点位路径不能为空，请重新设置所有路径')
                os.remove('config.ini')
                self.Config()
            elif not self.config.has_option('DEFAULT', 'gamepath') or not self.config.get('DEFAULT', 'gamepath'):
                messagebox.showwarning(title='提示', message='游戏路径不能为空，请重新设置所有路径')
                os.remove('config.ini')
                self.Config()
            else:
                pass
        else:
            self.config.read('config.ini')
            gamepath = self.config['DEFAULT']['gamepath']
            gameconfig.read(f'{gamepath}/config.ini')
            gametype = gameconfig['General']['cps']
            if gametype == 'bilibili':
                self.Gametype['values'] = ('b服转官服',)
            elif gametype == 'mihoyo' and os.path.exists(f'{gamepath}/YuanShen_Data'):
                self.Gametype['values'] = ('官服转b服', '官服转国际服')
            else:
                self.Gametype['values'] = ('国际服转官服',)
        self.config.set('DEFAULT', 'showupdate', 'disable')
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def ResetConfig(self):
        os.remove('config.ini')
        self.Config()


mainwindow = tk.Tk()
pt = PointSwitch(mainwindow)
mainwindow.mainloop()
