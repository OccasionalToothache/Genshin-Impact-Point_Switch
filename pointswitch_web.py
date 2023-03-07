import sys
import requests
import sqlite3
import os
import json
import qrcode
import shutil
import configparser
import socket
import atexit
from pywebio import start_server
from pywebio import config
from pywebio.input import *
from pywebio.output import *

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)



def main():
    clear('ROOT')
    scroll_to('ROOT')
    put_button(label='神瞳类', onclick=lambda: GetPoints('神瞳类')).style('text-align:center')
    put_button(label='宝箱类', onclick=lambda: GetPoints('宝箱类')).style('text-align:center')
    put_button(label='采集物', onclick=lambda: GetPoints('采集物')).style('text-align:center')
    put_button(label='怪物类', onclick=lambda: GetPoints('怪物类')).style('text-align:center')
    put_button(label='锄地类', onclick=lambda: GetPoints('锄地类')).style('text-align:center')
    put_button(label='清空点位', onclick=lambda: Clearpoint()).style('text-align:center')


def ExitWebMode():
    if os.path.exists('./qr.png'):
        os.remove('./qr.png')


def GetPoints(Pointstype):
    clear('ROOT')
    if not os.path.exists(f'./databases/{Pointstype}.db'):
        db = requests.get(f'http://www.pyforme.fun/{Pointstype}.db').content
        open(f'./databases/{Pointstype}.db', 'wb').write(db)
    conn = sqlite3.connect(f'./databases/{Pointstype}.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    forms = cursor.fetchall()
    i = []
    for form in forms:
        i.append(form[0])
    selection = select(label='点位名称', options=i)
    config = configparser.ConfigParser()
    config.read('config.ini')
    cheat = config['DEFAULT']['cheat']
    cheatpath = os.path.dirname(cheat)
    if not os.path.exists(f'{cheatpath}/teleports'):
        os.mkdir(f'{cheatpath}/teleports')
    else:
        shutil.rmtree(f'{cheatpath}/teleports')
        os.mkdir(f'{cheatpath}/teleports')
    conn = sqlite3.connect(f'./databases/{Pointstype}.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT 名称, 点位数据 FROM {selection}")
    rows = cursor.fetchall()
    for row in rows:
        name = row[0]
        data = json.loads(row[1])
        filename = name + '.json'
        with open(f'{cheatpath}/teleports/{filename}', 'w') as f:
            json.dump(data, f)
    conn.close()
    toast('切换成功！')
    main()


def Clearpoint():
    config = configparser.ConfigParser()
    config.read('config.ini')
    cheat = config['DEFAULT']['cheat']
    cheatpath = os.path.dirname(cheat)
    if not os.path.exists(f'{cheatpath}/teleports'):
        os.mkdir(f'{cheatpath}/teleports')
    else:
        shutil.rmtree(f'{cheatpath}/teleports')
        os.mkdir(f'{cheatpath}/teleports')
    toast('清空完毕')
    main()


def qr():
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f'http://{ip}:8080')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('qr.png')


atexit.register(ExitWebMode)
qr()
config(title='Pointswitch', theme='sketchy')
start_server(main, port=8080, debug=True)
