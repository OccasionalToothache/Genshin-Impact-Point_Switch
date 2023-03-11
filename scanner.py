import re
import requests
import cv2
import numpy as np
import win32gui
import win32con
import pyzbar.pyzbar as pyzbar
from PIL import ImageGrab
from tkinter import messagebox


def main(account):
    if account:
        WINDOW_NAME = "Scanner"
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        hwnd = win32gui.FindWindow(None, WINDOW_NAME)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        while True:
            screen = np.array(ImageGrab.grab(bbox=(700, 400, 1200, 800)))
            decoded_objects = pyzbar.decode(screen)
            if decoded_objects:
                for obj in decoded_objects:
                    x, y, w, h = obj.rect
                    cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow(WINDOW_NAME, screen)
            cv2.waitKey(1)
            if decoded_objects:
                url = re.findall(r"'(.*?)'", str(decoded_objects[0].data))[0]
                ticket = re.findall(r"ticket=(.*)", str(url))[0]
                break
        cv2.destroyAllWindows()
        datas = open(f'./scanner/{account}').readlines()
        uid = re.findall(r'uid:(.*)\n', datas[0])[0]
        device = re.findall(r'device:(.*)\n', datas[1])[0]
        token = re.findall(r'token:(.*)', datas[2])[0]
        data0 = {"app_id": 4, "device": f"{device}", "ticket": ticket}
        data1 = {"app_id": 4, "device": f"{device}",
                 "payload": {"proto": "Account", "raw": f'{{"uid":"{uid}","token":"{token}"}}'},
                 "ticket": ticket}
        session = requests.session()
        session.post(url='https://hk4e-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/scan', json=data0)
        session.post(url='https://hk4e-sdk.mihoyo.com/hk4e_cn/combo/panda/qrcode/confirm', json=data1)
    else:
        messagebox.showwarning(title='提示', message='请勾选扫码模式并切换一次账号')
