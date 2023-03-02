import subprocess
import winreg


class AccountChange:

    def __init__(self, gametype, account):
        self.account = account
        self.gametype = gametype

    def get_account(self):
        if self.gametype == '官服':
            key_path = r'SOFTWARE\miHoYo\原神'
            target = "MIHOYOSDK_ADL_PROD_CN_h3123967166"
        elif self.gametype == '国际服':
            key_path = r'SOFTWARE\miHoYo\Genshin Impact'
            target = "MIHOYOSDK_ADL_PROD_OVERSEA_h1158948810"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"{key_path}")
        general_data = winreg.QueryValueEx(key, "GENERAL_DATA_h2389025596")[0]
        miho_sdk = winreg.QueryValueEx(key, target)[0]
        general_data_hex = ",".join([f"{x:02x}" for x in general_data])
        miho_sdk_hex = ",".join([f"{x:02x}" for x in miho_sdk])
        reg_content = f"""Windows Registry Editor Version 5.00
        [HKEY_CURRENT_USER\\{key_path}]
        "GENERAL_DATA_h2389025596"=hex:{general_data_hex}
        "{target}"=hex:{miho_sdk_hex}"""
        with open(f"./accounts/{self.account}-{self.gametype}", "w") as reg_file:
            reg_file.write(reg_content)

    def change_account(self):
        if self.gametype == '官服':
            path = r'HKEY_CURRENT_USER\SOFTWARE\miHoYo\原神'
        elif self.gametype == '国际服':
            path = r'HKEY_CURRENT_USER\SOFTWARE\miHoYo\Genshin Impact'
        subprocess.run(["reg", "delete", path, "/f"])
        subprocess.call(f'reg import ./accounts/{self.account}')
