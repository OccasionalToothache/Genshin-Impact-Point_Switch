import atexit
import os
import shutil
import sys
import time
import psutil
import subprocess
import webbrowser
import threading
import accountchange
import requests
import sqlite3
import datetime
import configparser
import update_program
import tooltip
import tkinter as tk
from tkinter import simpledialog
from natsort import natsorted
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image,ImageTk


class PointSwitch:
    def __init__(self, master):
        self.Pointstype = None
        self.master = master
        self.config = None
        if not os.path.exists('./accounts'):
            os.mkdir('./accounts')
        self.accounts = os.listdir('./accounts')
        master.title('点位切换器v1.4.7')
        master.geometry('352x380+550+200')
        master.resizable(False, False)
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
        self.MainMenu.add_command(label='上传点位文件',command=lambda: self.Thread(webbrowser.open(url='http://www.pyforme.fun:4567')))
        self.MainMenu.add_command(label='清空点位文件', command=lambda: self.Thread(self.ClearPoints))
        self.AboutMenu.add_command(label='使用文档', command=lambda: self.Thread(webbrowser.open(url='http://www.pyforme.fun/read/manual.html')))
        self.AboutMenu.add_command(label='清除配置', command=lambda: self.Thread(self.ResetConfig))
        self.AboutMenu.add_command(label='web模式', command=lambda: self.Thread(self.WebMode()))
        self.MainMenu.add_cascade(label='查看更多内容', menu=self.AboutMenu)

    def MainUI(self):
        global var
        var = tk.BooleanVar()
        self.Oculus = tk.Button(master=self.master, text='神瞳类', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('神瞳类')))
        self.Oculus.place(x=20, y=20)
        self.Chests = tk.Button(master=self.master, text='宝箱类', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('宝箱类')))
        self.Chests.place(x=20, y=80)
        self.Items = tk.Button(master=self.master, text='采集物', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('采集物')))
        self.Items.place(x=20, y=140)
        self.Monsters = tk.Button(master=self.master, text='怪物类', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('怪物类')))
        self.Monsters.place(x=20, y=200)
        self.Auto = tk.Button(master=self.master, text='锄地类', font=('黑体', 18),command=lambda: self.Thread(self.GetPoints('锄地类')))
        self.Auto.place(x=20, y=260)
        self.PointsBox = tk.Listbox(master=self.master, height=9)
        self.Scrollbar = tk.Scrollbar(master=self.master, orient='vertical')
        self.PointsBox.config(yscrollcommand=self.Scrollbar.set)
        self.Scrollbar.config(command=self.PointsBox.yview)
        self.Scrollbar.place(x=307, y=22, height=163)
        self.PointsBox.place(x=180, y=20, width=145)
        self.Gametype = Combobox(master=self.master, width=15, state='readonly', font=('黑体', 12))
        self.Gametype.place(x=181, y=200)
        self.ChangePoint = tk.Button(master=self.master, text='换点', font=('黑体', 14),command=lambda: self.Thread(self.PointChange))
        self.ChangePoint.place(x=180, y=240)
        self.ChangeGametype = tk.Button(master=self.master, text='换服', font=('黑体', 14),command=lambda: self.Thread(self.GameTypeChange))
        self.ChangeGametype.place(x=270, y=240)
        self.Rename = tk.Checkbutton(master=self.master, text='是否为点位重命名', variable=var)
        self.Rename.place(x=180, y=280)
        tooltip.Tooltip(self.Rename, '如果出现点位乱序，则此功能会有帮助', topmost=True)
        self.Accountsbox = Combobox(master=self.master, width=36, state='readonly', font=('黑体', 12), values=self.accounts)
        self.Accountsbox.place(x=20, y=310)
        self.addaccount = tk.Button(master=self.master, text='添加账号', font=('黑体', 14), command=lambda: self.Addaccount())
        self.addaccount.place(x=20, y=340)
        tooltip.Tooltip(self.addaccount, '只能添加当前处于登录状态的账号', topmost=True)
        self.changeaccount = tk.Button(master=self.master, text='切换账号', font=('黑体', 14), command=lambda: self.Thread(self.Changeaccount))
        self.changeaccount.place(x=128, y=340)
        self.deleteaccount = tk.Button(master=self.master, text='删除账号', font=('黑体', 14), command=lambda: self.Thread(self.Deleteaccount))
        self.deleteaccount.place(x=236, y=340)

    def Thread(self, func):
        threading.Thread(target=func).start()

    def PackPoint(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        cheatpath = config['DEFAULT']['cheatpath']
        pointpath = filedialog.askdirectory(title='请选择需要打包的文件路径', initialdir=cheatpath)
        if pointpath:
            pointname = filedialog.asksaveasfilename(title='请选择文件保存的路径',initialfile=datetime.datetime.now().strftime('%H%M%S'),initialdir=cheatpath)
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
        if not os.path.exists('Pointswitch_Web.exe'):
            self.master.destroy()
            webmode = update_program.DownloadProgressBar('http://www.pyforme.fun/update/Pointswitch_Web.exe', './Pointswitch_Web.exe')
            webmode.start_download()
            webmode.root.title('正在下载Web模式组件')
            webmode.root.mainloop()
        if response != '1.4.7':
            if messagebox.askyesno(title='更新', message='检测到最新版本，是否更新'):
                self.master.destroy()
                update = update_program.DownloadProgressBar('http://www.pyforme.fun/update/Pointswitch.zip', './update.zip')
                update.start_download()
                update.root.mainloop()
            else:
                sys.exit()
        else:
            if os.path.exists('update.zip'):
                os.remove('update.zip')

    def GetPoints(self, Pointstype):
        self.Pointstype = Pointstype
        db = requests.get('http://www.pyforme.fun/Pt.db').content
        open('./Pt.db', 'wb').write(db)
        conn = sqlite3.connect('Pt.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {Pointstype}')
        names = cursor.fetchall()
        self.PointsBox.delete(first=0, last=tk.END)
        for name in names:
            self.PointsBox.insert(tk.END, name[0])
        cursor.close()
        conn.close()
        os.remove('Pt.db')

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
            global var
            if var.get():
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

    def WebMode(self):
        os.system('start Pointswitch_Web.exe')
        time.sleep(2)
        self.master.destroy()
        atexit.register(self.Restart)
        root = tk.Tk()
        root.geometry('350x350+500+200')
        root.title('请使用手机扫描二维码,结束Web模式请关闭此窗口')
        image = Image.open('./qr.png')
        img = ImageTk.PhotoImage(image)
        tk.Label(master=root, image=img).pack()
        root.mainloop()

    def Restart(self):
        for process in psutil.process_iter(['pid', 'name']):
            if process.name() == 'Pointswitch_Web.exe':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
        os.system('start Pointswitch.exe')

    def Addaccount(self):
        self.config = configparser.ConfigParser()
        gameconfig = configparser.ConfigParser()
        self.config.read('config.ini')
        gamepath = self.config['DEFAULT']['gamepath']
        gameconfig.read(f'{gamepath}/config.ini')
        gametype = gameconfig['General']['cps']
        if gametype == 'bilibili':
            pass
        elif gametype == 'mihoyo' and os.path.exists(f'{gamepath}/YuanShen_Data'):
            Gametype = '官服'
        else:
            Gametype = '国际服'
        try:
            ask = simpledialog.askstring(title='请为账号命名', prompt='请为账号命名', parent=self.master)
            if not ask == None:
                Ac = accountchange.AccountChange(Gametype, ask)
                Ac.get_account()
                self.Accountsbox['values'] = os.listdir('./accounts')
                messagebox.showinfo(title='提示', message='添加成功')

        except Exception:
            pass

    def Changeaccount(self):
        account = self.Accountsbox.get()
        try:
            if account:
               accountchange.AccountChange.change_account(account)
               messagebox.showinfo(title='提示', message='切换成功')
            else:
               messagebox.showinfo(title='提示', message='请选择一个账号')
        except Exception as e:
            print(e)
            messagebox.showinfo(title='错误', message='切换失败')

    def Deleteaccount(self):
        account = self.Accountsbox.get()
        os.remove(f'./accounts/{account}')
        self.Accountsbox['values'] = os.listdir('./accounts')
        self.Accountsbox.set('')
        messagebox.showinfo(title='提示', message='删除成功')


if __name__ == '__main__':
    mainwindow = tk.Tk()
    pt = PointSwitch(mainwindow)
    mainwindow.mainloop()
