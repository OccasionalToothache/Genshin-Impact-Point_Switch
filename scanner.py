import re
import requests
import cv2
import numpy as np
from PIL import ImageGrab
from tkinter import messagebox


def main(account):
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
                messagebox.showerror(title='错误', message='请求超时,请检查网络或关闭vpn代理')
    else:
        messagebox.showwarning(title='提示', message='请勾选扫码模式并切换一次账号')


# if __name__ == '__main__':
#     main('大号-官服-S')