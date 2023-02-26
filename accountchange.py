import subprocess
import os


class AccountChange:

    def __init__(self, gametype, account):
        self.account = account
        self.gametype = gametype

    def get_account(self):
        if self.gametype == '官服':
            registry_key = r'HKEY_CURRENT_USER\SOFTWARE\miHoYo\原神'
        elif self.gametype == '国际服':
            registry_key = r'HKEY_CURRENT_USER\SOFTWARE\miHoYo\Genshin Impact'
        subprocess.call(f'reg export "{registry_key}" "./accounts/{self.account}-{self.gametype}" /y')

    def change_account(self):
        subprocess.call(f'reg import ./accounts/{self}')

