import os
import atexit
import sys
import time
import tkinter as tk
import requests
import threading
from tkinter import messagebox


class DownloadProgressBar:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.root = tk.Tk()
        self.root.title("更新")
        self.root.geometry("300x100+578+280")
        self.root.protocol("WM_DELETE_WINDOW", self.unclose)
        self.create_widgets()

    def unclose(self):
        pass

    def updates(self):
        os.system('start update.bat')

    def create_widgets(self):
        self.progress_label = tk.Label(self.root, text="下载进度：0%")
        self.progress_label.pack(pady=10)
        self.progress_bar = tk.Canvas(self.root, width=250, height=25)
        self.progress_bar.pack()
        self.progress = 0
        self.cancelled = False

    def update_progress_bar(self):
        self.progress_bar.delete("all")
        self.progress_bar.create_rectangle(0, 0, 250 * self.progress / 100, 25, fill="orange")
        self.progress_label.config(text=f"下载进度：{self.progress:.1f}%")
        if self.progress < 100 and not self.cancelled:
            self.root.after(100, self.update_progress_bar)
        else:
            if not self.cancelled:
                messagebox.showinfo("下载完成", "文件已下载完成！")
                atexit.register(self.updates)
                sys.exit()

    def start_download(self):
        resp = requests.get('http://www.pyforme.fun/update/update.bat').content
        open('./update.bat', 'wb').write(resp)
        threading.Thread(target=self.download_file).start()
        self.update_progress_bar()

    def download_file(self):
        response = requests.get(self.url, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None:
            with open(self.filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        self.progress += len(chunk) / 1024 / 1024
        else:
            dl = 0
            total_length = int(total_length)
            with open(self.filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        dl += len(chunk)
                        f.write(chunk)
                        f.flush()
                        self.progress = dl / total_length * 100
