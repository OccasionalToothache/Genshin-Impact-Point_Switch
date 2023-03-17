# 原神点位切换器
### 打包方法：```pyinstaller point_switch1.6.8.spec``` 或者：```nuitka --windows-icon-from-ico=./ico.ico --windows-disable-console --onefile --standalone --enable-plugin=tk-inter --output-dir=out point_switch1.6.8.py
### 使用方法：下载releases的安装程序，请注意区分系统版本，不要安装在游戏目录或者作弊目录，选择游戏的启动程序和作弊程序，国际服的转换包需要额外下载，如果你出现注入失败，可以✓上防报错打开(使用此方式打开的作弊程序无法多开)，近期版本多开失败概率很高，等待后续版本更新
#### 如果您是高贵的win11用户，那么很遗憾的告诉您，这该死的系统无法多开作弊
#### 快捷键:F9打开扫码窗口，F10隐藏窗口, F11显示窗口, F12快速导出当前的账号配置(需手动重命名)
**视频教程：**

**快速扫码演示：http://www.pyforme.fun/preview.mp4 (注:视频演示为了展示效果所以使用窗口化，实际全屏化游戏也不会影响扫码)**  
**如何选择正确的路径：http://www.pyforme.fun/config.mp4 (如果选择错误可以通过清除配置进行修改，可以通过程序内清除或者删除程序目录下的config.ini文件**  
**如何切换点位： http://www.pyforme.fun/point_change.mp4 (如果没有作用，请确保选择的路径是否正确，并检查软件是否安装在teleports文件夹内)**   
**如何添加扫码登录的账号： http://www.pyforme.fun/scanner.mp4  (请确保没有使用任何vpn代理，在扫码框消失之后，请使用手机扫码正常登录一次账号才能获取到其他信息，请勿使用IOS系统的设备扫码登录,第一次使用等待时间较长，请耐心等待)**

### 如何添加扫码的账号信息(不要使用IOS系统的手机扫码)：
**首先你得有一款能使用F12控制台的浏览器，这里使用的是windows自带的Edge浏览器，登录米哈游通行证：https://user.mihoyo.com**
**点击登录设备这一选项，记住自己的设备名称**
![4](images/4.png)
**接着按下F12打开浏览器控制台，选择网络，选择Fetch/XHR，按下F5或者右键刷新网页**  
![5](images/5.png)
**找到名称为list开头的选项，选择预览，依次展开data下的devices，可以看到对应设备的device数值，复制数值即可，不要复制其他任何标点符号**
![6](images/6.png)  
**获取到device之后回到切换器，勾选扫码模式并点击添加账号，输入账号的名称，粘贴刚刚复制的device数值，会弹出一个扫码窗口，此时打开原神，选择二维码登录，然后使用米游社/手机原神/云原神正常扫码登录即可保存账号信息**
![7](images/7.png)
