from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from tkinter import messagebox
import requests
import time
import pyperclip


def main():
    browser = webdriver.ChromiumEdge()
    browser.get('https://user.mihoyo.com/#/login/password')
    checkbutton = browser.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[1]/div/p/div')
    checkbutton.click()
    WebDriverWait(browser, 3600).until(expected_conditions.url_contains('https://user.mihoyo.com/#/account/home'))
    devicebutton = browser.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[1]/div[1]/ul/li[7]')
    devicebutton.click()
    cookies = browser.get_cookies()
    cookie = {
        'login_ticket': cookies[0]['value'],
        'DEVICEFP_SEED_TIME': cookies[1]['value'],
        'login_uid': cookies[2]['value'],
        'DEVICEFP': cookies[3]['value'],
        'DEVICEFP_SEED_ID': cookies[4]['value'],
        '_MHYUUID': cookies[5]['value']
    }
    time.sleep(0.5)
    logs = browser.execute_script('return window.performance.getEntries()')
    for log in logs:
        url = log['name']
        if 'https://api-takumi.mihoyo.com/device/api/list' in url:
            resp = requests.get(url=url, cookies=cookie).json()
            devices = resp['data']['devices']
            for device in devices:
                if device['client'] == 3:
                    pyperclip.copy(device["device_id"])
                    messagebox.showinfo(title='提示', message='device已复制到剪切板')
                    break
    browser.quit()

