# -*- coding: utf-8 -*-
import atexit
import os
import pythoncom
import json
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
import scanner
import update_program
import tooltip
import keyboard
import tkinter as tk
import add_scan_account
import win32com.client
from tkinter import simpledialog
from natsort import natsorted
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk


class PointSwitch:
    def __init__(self, master):
        self.Pointstype = None
        self.master = master
        self.config = None
        self.sc_account = None
        if not os.path.exists('./accounts'):
            os.mkdir('./accounts')
        if not os.path.exists('./databases'):
            os.mkdir('./databases')
        if not os.path.exists('./scanner'):
            os.mkdir('./scanner')
        self.accounts = os.listdir('./accounts')
        master.title('点位切换器1.6.9')
        master.geometry('352x380+550+200')
        master.resizable(False, False)
        master.iconbitmap(default='ico.ico')
        self.Menus()
        self.MainUI()
        self.Config()
        self.CheckUpdate()
        self.start_hotkey_thread()
        self.pack_buttons()
        atexit.register(self.on_closing)

    def Menus(self):
        self.MainMenu = tk.Menu(self.master)
        self.master.config(menu=self.MainMenu)
        self.AboutMenu = tk.Menu(self.MainMenu, tearoff=0)
        self.MainMenu.add_command(label='打包点位文件', command=lambda: self.Thread(self.PackPoint))
        self.MainMenu.add_command(label='上传点位文件',command=lambda: webbrowser.open(url='http://www.pyforme.fun:4567'))
        self.MainMenu.add_command(label='清空点位文件', command=lambda: self.Thread(self.ClearPoints))
        self.AboutMenu.add_command(label='使用文档', command=lambda: webbrowser.open(url='https://github.com/GC-Ruth/Genshin-Impact-Point_Switch#readme'))
        self.AboutMenu.add_command(label='清除配置', command=lambda: self.Thread(self.ResetConfig))
        self.MainMenu.add_cascade(label='查看更多内容', menu=self.AboutMenu)

    def MainUI(self):
        global var, startmode, error, scan
        var = tk.BooleanVar()
        startmode = tk.BooleanVar()
        error = tk.BooleanVar()
        scan = tk.BooleanVar()
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
        self.Gametype.place(x=181, y=195)
        self.ChangePoint = tk.Button(master=self.master, text='换点', font=('黑体', 14),command=lambda: self.Thread(self.PointChange))
        self.ChangePoint.place(x=195, y=240)
        self.ChangeGametype = tk.Button(master=self.master, text='换服', font=('黑体', 14),command=lambda: self.Thread(self.GameTypeChange))
        self.ChangeGametype.place(x=265, y=240)
        self.Rename = tk.Checkbutton(master=self.master, text='是否为点位重命名', variable=var)
        self.Rename.place(x=220, y=280)
        tooltip.Tooltip(self.Rename, '如果出现点位乱序，则此功能会有帮助', topmost=True)
        self.Accountsbox = Combobox(master=self.master, width=24, state='readonly', font=('黑体', 12), values=self.accounts)
        self.Accountsbox.place(x=20, y=310)
        self.StartGame = tk.Button(master=self.master, width=9, text='启动游戏', font=('黑体', 12), command=lambda: self.Thread(self.Start))
        self.StartGame.place(x=245, y=306)
        tooltip.Tooltip(self.StartGame, '如无法正常启动多个游戏程序,请手动开启', topmost=True)
        self.addaccount = tk.Button(master=self.master, text='添加账号', font=('黑体', 14), command=lambda: self.Thread(self.Addaccount(hotkey=None)))
        self.addaccount.place(x=20, y=340)
        tooltip.Tooltip(self.addaccount, '添加当前处于登录状态的账号,快捷键F12', topmost=True)
        self.changeaccount = tk.Button(master=self.master, text='切换账号', font=('黑体', 14), command=lambda: self.Thread(self.Changeaccount))
        self.changeaccount.place(x=128, y=340)
        tooltip.Tooltip(self.changeaccount, '多开时请等待账号登陆之后再切换新账号\n否则会直接登录新账号')
        self.deleteaccount = tk.Button(master=self.master, text='删除账号', font=('黑体', 14), command=lambda: self.Thread(self.Deleteaccount))
        self.deleteaccount.place(x=236, y=340)
        self.duokai = tk.Checkbutton(master=self.master, text='多开', command=lambda: self.Thread(self.Duokai))
        tooltip.Tooltip(self.duokai, '需要管理员权限,登录账号的时候请取消勾选，否则无法联网', topmost=True)
        self.cheat = tk.Checkbutton(master=self.master, text='作弊', variable=startmode)
        tooltip.Tooltip(self.cheat, '使用作弊程序启动游戏', topmost=True)
        self.er = tk.Checkbutton(master=self.master, text='防报错', variable=error)
        tooltip.Tooltip(self.er, '如果你无法注入,勾选此项可能会有帮助')
        self.sc = tk.Checkbutton(master=self.master, text='扫码模式', variable=scan, command=lambda: self.Thread(self.cg))
        tooltip.Tooltip(self.sc, '勾选之后需要切换账号才会生效,F9开启,ESC退出')

    def pack_buttons(self):
        buttons = requests.get(url='http://www.pyforme.fun/buttons.html').json()
        if buttons['duokai'] == 'on':
            self.duokai.place(x=118, y=280)
        if buttons['cheat'] == 'on':
            self.cheat.place(x=170, y=280)
        if buttons['scanner'] == 'on':
            self.sc.place(x=118, y=220)
        if buttons['error'] == 'on':
            self.er.place(x=118, y=250)
        if buttons['web'] == 'on':
            self.AboutMenu.add_command(label='web模式', command=lambda: self.Thread(self.WebMode()))

    def Thread(self, func):
        try:
            t = threading.Thread(target=func, daemon=True)
            t.start()
        except Exception as e:
            print(e)

    def cg(self):
        global scan
        if scan.get():
            self.Accountsbox['value'] = os.listdir('./scanner')
            self.Accountsbox.set('')
        else:
            self.Accountsbox['value'] = os.listdir('./accounts')
            self.Accountsbox.set('')

    def PackPoint(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        cheat = config['DEFAULT']['cheat']
        cheatpath = os.path.dirname(cheat)
        pointpath = filedialog.askdirectory(title='请选择需要打包的文件路径', initialdir=cheatpath)
        if pointpath:
            pointname = filedialog.asksaveasfilename(title='请选择文件保存的路径',initialfile=datetime.datetime.now().strftime('%H%M%S'),initialdir=cheatpath)
            if pointname:
                shutil.make_archive(pointname, 'zip', pointpath)
                messagebox.showinfo(title='提示', message=f'点位文件已成功打包到{pointname}')

    def ClearPoints(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        cheat = self.config['DEFAULT']['cheat']
        cheatpath = os.path.dirname(cheat)
        if not os.path.exists(f'{cheatpath}/teleports'):
            os.mkdir(f'{cheatpath}/teleports')
        else:
            shutil.rmtree(f'{cheatpath}/teleports')
            os.mkdir(f'{cheatpath}/teleports')
        messagebox.showinfo(title='提示', message='点位文件夹已清空')

    def CheckUpdate(self):
        response = requests.get(url='http://www.pyforme.fun/update.html').text
        if not os.path.exists('Pointswitch_Web-v1.1.exe'):
            self.master.destroy()
            webmode = update_program.DownloadProgressBar('http://www.pyforme.fun/update/Pointswitch_Web.exe', './Pointswitch_Web-v1.1.exe')
            webmode.start_download()
            webmode.root.title('正在下载Web模式组件')
            webmode.root.mainloop()
        if response != '1.6.9':
            if messagebox.askyesno(title='更新', message='检测到最新版本，是否更新'):
                self.master.destroy()
                atexit.register(lambda: os.system('start update.exe'))
                update = update_program.DownloadProgressBar('http://www.pyforme.fun/update/Pointswitch_Setup.exe', './update.exe')
                update.start_download()
                update.root.mainloop()
            else:
                sys.exit()
        else:
            if os.path.exists('update.exe'):
                os.remove('update.exe')

    def download_database(self, Pointstype):
        db = requests.get(f'http://www.pyforme.fun/{Pointstype}.db').content
        open(f'./databases/{Pointstype}.db', 'wb').write(db)
        self.master.after(0, self.update_points_box, Pointstype)

    def update_points_box(self, Pointstype):
        conn = sqlite3.connect(f'./databases/{Pointstype}.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        names = cursor.fetchall()
        self.PointsBox.delete(first=0, last=tk.END)
        for name in names:
            self.PointsBox.insert(tk.END, name[0])
        cursor.close()
        conn.close()

    def GetPoints(self, Pointstype):
        self.Pointstype = Pointstype
        if not os.path.exists(f'./databases/{Pointstype}.db'):
            t = threading.Thread(target=self.download_database, args=(Pointstype,), daemon=True)
            t.start()
        else:
            self.update_points_box(Pointstype)

    def PointChange(self):
        Selection = self.PointsBox.curselection()
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        cheat = self.config['DEFAULT']['cheat']
        cheatpath = os.path.dirname(cheat)
        if Selection:
            if not os.path.exists(f'{cheatpath}/teleports'):
                os.mkdir(f'{cheatpath}/teleports')
            else:
                shutil.rmtree(f'{cheatpath}/teleports')
                os.mkdir(f'{cheatpath}/teleports')
            conn = sqlite3.connect(f'./databases/{self.Pointstype}.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT 名称, 点位数据 FROM {self.PointsBox.get(Selection[0])}")
            rows = cursor.fetchall()
            for row in rows:
                name = row[0]
                data = json.loads(row[1])
                filename = name + '.json'
                with open(f'{cheatpath}/teleports/{filename}', 'w') as f:
                    json.dump(data, f)
            conn.close()
            global var
            if var.get():
                folder_path = f'{cheatpath}/teleports'
                file_names = os.listdir(folder_path)
                json_file_names = natsorted([f for f in file_names if f.endswith('.json')])
                for i, json_file_name in enumerate(json_file_names):
                    new_json_file_name = '{:04d}.json'.format(i + 1)
                    os.rename(os.path.join(folder_path, json_file_name), os.path.join(folder_path, new_json_file_name))
            messagebox.showinfo(title='提示', message=f'点位{self.PointsBox.get(Selection[0])}切换成功')
        else:
            messagebox.showwarning(title='提示', message='请选择一个点位')

    def Duokai(self):
        domain_names = open('./hoyohosts', 'r').readlines()
        config = configparser.ConfigParser()
        config.read('config.ini')
        game = config['DEFAULT']['game']
        gamepath = os.path.dirname(game)
        hosts_path = 'C:/Windows/System32/drivers/etc/hosts'
        backup_path = 'C:/Windows/System32/drivers/etc/hosts.bak'
        try:
            if os.path.exists(f'{gamepath}/mhypbase.dll') and os.path.exists(hosts_path):
                shutil.copy2(hosts_path, backup_path)
                with open(hosts_path, 'a') as hosts:
                    for domain_name in domain_names:
                        hosts.write(f'{domain_name}')
                os.rename(f'{gamepath}/mhypbase.dll', f'{gamepath}/fuck')
            elif os.path.exists(f'{gamepath}/fuck') and os.path.exists(backup_path):
                os.remove(hosts_path)
                os.rename(backup_path, hosts_path)
                os.rename(f'{gamepath}/fuck', f'{gamepath}/mhypbase.dll')
        except Exception:
            messagebox.showwarning(title='警告', message='多开失败,请确保权限足够')

    def Start(self):
        global startmode
        global error
        config = configparser.ConfigParser()
        config.read('config.ini')
        game = config['DEFAULT']['game']
        gamepath = os.path.dirname(game)
        cheat = config['DEFAULT']['cheat']
        if os.path.exists(f'{gamepath}/YuanShen.exe') and not startmode.get():
            subprocess.run([f'{gamepath}/YuanShen.exe'], cwd=gamepath, shell=True)
        elif os.path.exists(f'{gamepath}/GenshinImpact.exe') and not startmode.get():
            subprocess.run([f'{gamepath}/GenshinImpact.exe'], cwd=gamepath, shell=True)
        elif error.get():
            if not os.path.exists('./Akeni.lnk'):
                self.create_shortcut(cheat, './Akebi.lnk', '-analog_inject')
                subprocess.run(['Akebi.lnk'], shell=True)
        elif startmode.get():
            subprocess.run(cheat, shell=True)

    def GameTypeChange(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        game = self.config['DEFAULT']['game']
        cheat = self.config['DEFAULT']['cheat']
        cheatpath = os.path.dirname(cheat)
        gamepath = os.path.dirname(game)
        Value = self.Gametype.get()
        if Value == '官服转b服':
            shutil.unpack_archive(filename='./data/官转b.zip', extract_dir=gamepath)
            messagebox.showinfo(title='提示', message='已成功从官服转为b服')
        elif Value == 'b服转官服':
            shutil.unpack_archive(filename='./data/b转官.zip', extract_dir=gamepath)
            os.remove(f'{gamepath}/YuanShen_Data/Plugins/PCGameSDK.dll')
            messagebox.showinfo(title='提示', message='已成功从b服转为官服')
        elif Value == '官服转国际服':
            if not os.path.exists('./data/官转国3.5.zip'):
                if messagebox.askyesno(title='提示', message='未检测到官转国依赖包，是否前往下载'):
                    webbrowser.open(url='https://pan.baidu.com/s/1w1LYakMPpyuIAv5MWCJDrA?pwd=si1t')
            else:
                try:
                    self.revalue(1)
                    os.rename(f'{gamepath}/YuanShen_Data', f'{gamepath}/GenshinImpact_Data')
                    os.remove(f'{gamepath}/YuanShen.exe')
                    shutil.unpack_archive(filename='./data/官转国3.5.zip', extract_dir=gamepath)
                    if os.path.exists(f'{cheatpath}/cfg.ini'):
                        os.remove(f'{cheatpath}/cfg.ini')
                    with open(f'{cheatpath}/cfg.ini', 'w') as file:
                        file.write("[GenshinImpact]\nPath = F:\yuanshen\Genshin Impact\Genshin Impact Game\GenshinImpact.exe")
                    self.config.set('DEFAULT', 'game', f'{gamepath}/GenshinImpact.exe')
                    self.config.set('DEFAULT', 'cheat', f'{cheat}')
                    with open('config.ini', 'w') as f:
                        self.config.write(f)
                    messagebox.showinfo(title='提示', message='已成功从官服转为国际服')
                    self.Config()
                except Exception as e:
                    print(e)
        elif Value == '国际服转官服':
            if not os.path.exists('./data/国转官3.5.zip'):
                if messagebox.askyesno(title='提示', message='未检测到国转官依赖包，是否前往下载'):
                    webbrowser.open(url='https://pan.baidu.com/s/1w1LYakMPpyuIAv5MWCJDrA?pwd=si1t')
            else:
                try:
                    self.revalue(1)
                    os.rename(f'{gamepath}/GenshinImpact_Data', f'{gamepath}/YuanShen_Data')
                    os.remove(f'{gamepath}/GenshinImpact.exe')
                    shutil.unpack_archive(filename='./data/国转官3.5.zip', extract_dir=gamepath)
                    if os.path.exists(f'{cheatpath}/cfg.ini'):
                        os.remove(f'{cheatpath}/cfg.ini')
                    with open(f'{cheatpath}/cfg.ini', 'w') as file:
                        file.write("[GenshinImpact]\nPath = F:\yuanshen\Genshin Impact\Genshin Impact Game\YuanShen.exe")
                    self.config.set('DEFAULT', 'game', f'{gamepath}/YuanShen.exe')
                    self.config.set('DEFAULT', 'cheat', f'{cheat}')
                    with open('config.ini', 'w') as f:
                        self.config.write(f)
                    messagebox.showinfo(title='提示', message='已成功从国际服转为官服')
                    self.Config()
                except Exception as e:
                    print(e)
        else:
            messagebox.showwarning(title='提示', message='请选择一个选项')
        self.Config()

    def Config(self):
        self.config = configparser.ConfigParser()
        gameconfig = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            game = filedialog.askopenfilename(title='请选择YuanShen.exe或者GenshinImpact.exe', filetypes=(("Executable files", "*.exe"),), initialdir='请选择YuanShen.exe或者GenshinImpact.exe')
            self.config.set('DEFAULT', 'game', game)
            if 'YuanShen.exe' in game or 'GenshinImpact.exe' in game:
                cheat = filedialog.askopenfilename(title='请选择指定的作弊程序', filetypes=(("Executable files", "*.exe"),), initialdir='请选择指定的作弊程序')
                self.config.set('DEFAULT', 'cheat', cheat)
                if not cheat == '':
                    with open('config.ini', 'w') as configfile:
                        self.config.write(configfile)
                else:
                    sys.exit()
            elif game == '':
                sys.exit()
            else:
                messagebox.showwarning(title='提示', message='请选择正确的游戏程序')
                self.Config()
        else:
            self.config.read('config.ini')
            game = self.config['DEFAULT']['game']
            gamepath = os.path.dirname(game)
            gameconfig.read(f'{gamepath}/config.ini')
            gametype = gameconfig['General']['cps']
            if gametype == 'bilibili':
                self.Gametype['values'] = ('b服转官服',)
            elif gametype == 'mihoyo' and os.path.exists(f'{gamepath}/YuanShen_Data'):
                self.Gametype['values'] = ('官服转b服', '官服转国际服')
            else:
                self.Gametype['values'] = ('国际服转官服',)

    def ResetConfig(self):
        os.remove('config.ini')
        self.Config()

    def WebMode(self):
        global root
        os.system('start Pointswitch_Web-v1.1.exe')
        time.sleep(2)
        self.master.destroy()
        root = tk.Tk()
        root.geometry('350x350+500+200')
        root.title('请使用手机扫描二维码,结束Web模式请关闭此窗口')
        root.protocol('WM_DELETE_WINDOW', self.Restart)
        image = Image.open('./qr.png')
        img = ImageTk.PhotoImage(image)
        tk.Label(master=root, image=img).pack()
        root.mainloop()

    def Restart(self):
        global root
        root.destroy()
        for process in psutil.process_iter(['pid', 'name']):
            if process.name() == 'Pointswitch_Web-v1.1.exe':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
        os.system('start Pointswitch.exe')


    def Addaccount(self, hotkey):
        global scan
        self.config = configparser.ConfigParser()
        gameconfig = configparser.ConfigParser()
        self.config.read('config.ini')
        game = self.config['DEFAULT']['game']
        gamepath = os.path.dirname(game)
        gameconfig.read(f'{gamepath}/config.ini')
        gametype = gameconfig['General']['cps']
        if gametype == 'bilibili':
            Gametype = 'b服'
            messagebox.showinfo(title='提示', message='暂时不支持添加b服账号')
        elif gametype == 'mihoyo' and os.path.exists(f'{gamepath}/YuanShen_Data'):
            Gametype = '官服'
        else:
            Gametype = '国际服'
        try:
            if hotkey != 'f12' and not Gametype == 'b服':
                ask = simpledialog.askstring(title='请为账号命名', prompt='请为账号命名', parent=self.master)
            else:
                ask = '未命名'
            if not ask == None and not hotkey == 'f12' and not Gametype == 'b服':
                if not scan.get():
                    Ac = accountchange.AccountChange(Gametype, ask)
                    Ac.get_account()
                    self.Accountsbox['values'] = os.listdir('./accounts')
                    messagebox.showinfo(title='提示', message='添加成功')
                else:
                    self.Thread(self.add_scan(ask))
                    self.Accountsbox['values'] = os.listdir('./scanner')
            else:
                Ac = accountchange.AccountChange(Gametype, ask)
                Ac.get_account()
        except Exception:
            pass

    def add_scan(self, name):
        try:
            self.master.withdraw()
            add_scan_account.main()
            self.master.deiconify()
            device = simpledialog.askstring(title='提示', prompt='请输入获取的device', parent=self.master)
            if not device == None:
                self.master.withdraw()
                self.Thread(scanner.addaccount(device, name))
                self.master.deiconify()
                messagebox.showinfo(title='提示', message='添加成功')
        except Exception:
            messagebox.showinfo(title='提示', message='添加失败')
            self.master.deiconify()

    def Changeaccount(self):
        global scan
        self.config = configparser.ConfigParser()
        gameconfig = configparser.ConfigParser()
        self.config.read('config.ini')
        game = self.config['DEFAULT']['game']
        gamepath = os.path.dirname(game)
        gameconfig.read(f'{gamepath}/config.ini')
        gametype = gameconfig['General']['cps']
        if gametype == 'bilibili':
            pass
        elif gametype == 'mihoyo' and os.path.exists(f'{gamepath}/YuanShen_Data'):
            Gametype = '官服'
        else:
            Gametype = '国际服'
        account = self.Accountsbox.get()
        try:
            if account:
                if not scan.get():
                   ac = accountchange.AccountChange(Gametype, account)
                   ac.change_account()
                else:
                    self.sc_account = account
                messagebox.showinfo(title='提示', message='切换成功')
            else:
               messagebox.showinfo(title='提示', message='请选择一个账号')
        except Exception as e:
            print(e)
            messagebox.showinfo(title='错误', message='切换失败')

    def Deleteaccount(self):
        global scan
        account = self.Accountsbox.get()
        if account:
            if messagebox.askyesno(title='提示', message=f'请确认是否删除账号：{account}'):
                if not scan.get():
                    os.remove(f'./accounts/{account}')
                    self.Accountsbox['values'] = os.listdir('./accounts')
                    self.Accountsbox.set('')
                else:
                    os.remove(f'./scanner/{account}')
                    self.Accountsbox['values'] = os.listdir('./scanner')
                    self.Accountsbox.set('')
                messagebox.showinfo(title='提示', message='删除成功')
        else:
            messagebox.showwarning(title='警告', message='请选中一个账号')

    def revalue(self, type):
        hosts_path = 'C:/Windows/System32/drivers/etc/hosts'
        backup_path = 'C:/Windows/System32/drivers/etc/hosts.bak'
        config = configparser.ConfigParser()
        config.read('config.ini')
        game = config['DEFAULT']['game']
        gamepath = os.path.dirname(game)
        if os.path.exists(f'{gamepath}/fuck') and os.path.exists(backup_path):
            os.remove(hosts_path)
            os.rename(backup_path, hosts_path)
            os.rename(f'{gamepath}/fuck', f'{gamepath}/mhypbase.dll')
            if type == 1:
                self.duokai.deselect()

    def hotkeys(self):
        keyboard.add_hotkey('f12', lambda: self.Addaccount('f12'))
        keyboard.add_hotkey('f10', self.master.withdraw)
        keyboard.add_hotkey('f11', self.master.deiconify)
        keyboard.add_hotkey('f9', lambda: scanner.login(self.sc_account))
        keyboard.wait()

    def start_hotkey_thread(self):
        hotkey_thread = threading.Thread(target=self.hotkeys, daemon=True)
        hotkey_thread.start()

    def on_closing(self):
        self.revalue(0)
        shutil.rmtree('./databases')
        os.mkdir('./databases')

    def create_shortcut(self, target_path, shortcut_path, arguments=None):
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = target_path
        if arguments:
            shortcut.Arguments = arguments
        shortcut.save()


if __name__ == '__main__':
    mainwindow = tk.Tk()
    pt = PointSwitch(mainwindow)
    mainwindow.mainloop()
