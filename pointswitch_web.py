import sys
import requests
import sqlite3
import os
import qrcode
import shutil
import configparser
import socket
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
    put_button(label='切换服务器', onclick=lambda: GameTypeChange()).style('text-align:center')


def ExitWebMode():
    clear('ROOT')
    sys.exit()


def GetPoints(Pointstype):
    clear('ROOT')
    db = requests.get('http://www.pyforme.fun/Pt.db').content
    open('./Pt.db', 'wb').write(db)
    conn = sqlite3.connect('Pt.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {Pointstype}')
    names = cursor.fetchall()
    selection = select(label='点位名称', options=names)
    config = configparser.ConfigParser()
    config.read('config.ini')
    response = requests.get(url=selection).content
    open('data.zip', 'wb').write(response)
    if os.path.exists(f'{config["DEFAULT"]["cheatpath"]}/teleports'):
        shutil.rmtree(f'{config["DEFAULT"]["cheatpath"]}/teleports')
    shutil.unpack_archive(filename='data.zip', extract_dir=f'{config["DEFAULT"]["cheatpath"]}/teleports')
    os.remove('data.zip')
    toast('切换成功！')
    cursor.close()
    conn.close()
    os.remove('Pt.db')
    main()


def Clearpoint():
    config = configparser.ConfigParser()
    config.read('config.ini')
    cheatpath = config['DEFAULT']['cheatpath']
    if not os.path.exists(f'{cheatpath}/teleports'):
        os.mkdir(f'{cheatpath}/teleports')
    else:
        shutil.rmtree(f'{cheatpath}/teleports')
        os.mkdir(f'{cheatpath}/teleports')
    toast('清空完毕')
    main()


def GameTypeChange():
    clear('ROOT')
    config = configparser.ConfigParser()
    config.read('config.ini')
    gamepath = config['DEFAULT']['gamepath']
    typelist = ['官服转b服', 'b服转官服', '官服转国际服', '国际服转官服']
    Value = select(label='请选择转换的服务器', options=typelist)
    if Value == '官服转b服':
        shutil.unpack_archive(filename='./data/官转b.zip', extract_dir=gamepath)
        os.remove(f'{gamepath}/YuanShen_Data/Plugins/metakeeper.dll')
        toast('已成功从官服转为b服')
        main()
    elif Value == 'b服转官服':
        shutil.unpack_archive(filename='./data/b转官.zip', extract_dir=gamepath)
        os.remove(f'{gamepath}/YuanShen_Data/Plugins/PCGameSDK.dll')
        toast('已成功从b服转为官服')
        main()
    elif Value == '官服转国际服':
        if not os.path.exists('./data/官转国3.4.zip'):
            toast('未检测到官转国依赖包,请前往下载')
            main()
        else:
            put_loading('border', 'dark').style('position: relative;top: 200px;left: 170px')
            os.rename(f'{gamepath}/YuanShen_Data', f'{gamepath}/GenshinImpact_Data')
            os.remove(f'{gamepath}/YuanShen.exe')
            shutil.unpack_archive(filename='./data/官转国3.4.zip', extract_dir=gamepath)
            toast('已成功从官服转为国际服')
            main()
    elif Value == '国际服转官服':
        if not os.path.exists('./data/国转官3.4.zip'):
            toast('为检测到国转官依赖包,请前往下载')
            main()
        else:
            put_loading('border', 'dark').style('position: relative;top: 200px;left: 170px')
            os.rename(f'{gamepath}/GenshinImpact_Data', f'{gamepath}/YuanShen_Data')
            os.remove(f'{gamepath}/GenshinImpact.exe')
            shutil.unpack_archive(filename='./data/国转官3.4.zip', extract_dir=gamepath)
            toast('已成功从国际服转为官服')
            main()


def qr():
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f'http://{ip}:8080')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('qr.png')


qr()
config(title='Pointswitch', theme='yeti')
# start_server(main, port=8080, debug=True)
