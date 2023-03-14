import re
import requests
import cv2
import numpy as np
import time
from PIL import ImageGrab
from tkinter import messagebox


def login(account):
    if account:
        detector = cv2.QRCodeDetector()
        WINDOW_NAME = "Scanner"
        SCAN_AREA = (700, 400, 1200, 800)
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_TOPMOST, 1)
        cv2.resizeWindow(WINDOW_NAME, 500, 400)
        while True:
            screen = np.array(ImageGrab.grab(bbox=SCAN_AREA))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            data, bbox, _ = detector.detectAndDecode(gray)
            if data:
                break
            cv2.imshow(WINDOW_NAME, screen)
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()
        if data:
            ticket = re.findall(r'ticket=(.*)', data)[0]
            datas = open(f'./scanner/{account}').readlines()
            uid = re.findall(r'uid:(.*)\n', datas[0])[0]
            device = re.findall(r'device:(.*)\n', datas[1])[0]
            token = re.findall(r'token:(.*)', datas[2])[0]
            data0 = {"app_id": 4, "device": f"{device}", "ticket": ticket}
            data1 = {"app_id": 4, "device": f"{device}",
                     "payload": {"proto": "Account", "raw": f'{{"uid":"{uid}","token":"{token}"}}'},
                     "ticket": ticket}
            session = requests.session()
            try:
                session.post(url='https://hk4e-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/scan', json=data0, timeout=5)
                session.post(url='https://hk4e-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/confirm', json=data1, timeout=5)
            except Exception:
                messagebox.showinfo(title='错误', message='请求超时,请检查网络连接或关闭vpn代理,并重启程序')
    else:
        messagebox.showinfo(title='提示', message='请勾选扫码模式并切换一次账号')


def addaccount(device, name, gametype):
    detector = cv2.QRCodeDetector()
    WINDOW_NAME = "Scanner"
    SCAN_AREA = (700, 400, 1200, 800)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_TOPMOST, 1)
    cv2.resizeWindow(WINDOW_NAME, 500, 400)
    while True:
        screen = np.array(ImageGrab.grab(bbox=SCAN_AREA))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        data, bbox, _ = detector.detectAndDecode(gray)
        if data:
            break
        cv2.imshow(WINDOW_NAME, screen)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    if data:
        ticket = re.findall(r'ticket=(.*)', data)[0]
    data = {"app_id": 4, "device": f"{device}", "ticket": f"{ticket}"}
    while True:
        try:
            response = requests.post(url='https://hk4e-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/query?', json=data, timeout=5).json()
        except Exception:
            messagebox.showinfo(title='提示', message='请求超时,请检查网络连接或关闭VPN代理,并重启程序')
            print(response)
        if response['message'] == 'ExpiredCode':
            messagebox.showinfo(title='提示', message='二维码已失效,请重新扫描')
            break
        elif response['data']['stat'] == 'Confirmed':
            uid = re.findall(r'"uid":"(.*?)"', response['data']['payload']['raw'])[0]
            token = re.findall(r'"token":"(.*?)"', response['data']['payload']['raw'])[0]
            with open(f'./scanner/{name}-{gametype}-S', 'w', encoding='utf-8') as file:
                file.write(f'uid:{uid}\ndevice:{device}\ntoken:{token}')
            break
        time.sleep(1)

