import os
import re
import subprocess
import sys

import requests
import urllib3

urllib3.disable_warnings()
from colorama import init, Fore, Back, Style

init(autoreset=True)
RootPath = os.path.dirname(__file__)

black_suffix = ['png', 'gif', 'jpg', 'jpeg', 'css', 'ico', 'js', 'woff', 'svg', 'woff2']   # 过滤后缀名
black_list = ['fonts', 'css']                                                              # 过滤末尾目录名


class Log(object):
    def red(self, s):
        return Fore.RED + s + Fore.RESET

    def green(self, s):
        return Fore.GREEN + s + Fore.RESET

    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET

    def blue(self, s):
        return Fore.BLUE + s + Fore.RESET

    def magenta(self, s):
        return Fore.MAGENTA + s + Fore.RESET

    def cyan(self, s):
        return Fore.CYAN + s + Fore.RESET

    def white(self, s):
        return Fore.WHITE + s + Fore.RESET

    def black(self, s):
        return Fore.BLACK

    def white_green(self, s):
        return Fore.WHITE + Back.GREEN + s

    def dave(self, s):
        return Style.BRIGHT + Fore.GREEN + s


def hum_convert(value):
    units = ["B", "KB", "MB", "GB", "TB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size


def req(sub, url):
    color = Log()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    global title
    try:
        if "GET" in sub:
            res = requests.get(url, headers=headers, timeout=4, verify=False)
        else:
            res = requests.post(url, headers=headers, timeout=4, verify=False)

        code = res.apparent_encoding
        res.encoding = code
        try:
            title = re.findall("<title>.*?</title>", res.text)[0].replace("<title>", '').replace("</title>", '')
        except IndexError:
            tilte = ""

        length = hum_convert(len(res.text))
        if res.status_code == 200:
            print(color.green(f"[{sub}]  [200] [{length}]  [{url}] [{title}]"))
        elif res.status_code == 404:
            print(color.blue(f"[{sub}]  [404] [{length}]  [{url}] [{title}]"))
        else:
            print(color.cyan(f"[{sub}]  [{res.status_code}] [{length}]  [{url}] [{title}]"))

    except Exception as error:
        print(color.red(f"[{sub}]   [0] [0KB]   [{url}]"))


def run(target):
    data = []
    options = f"{RootPath}\\rad.exe -t {target}"
    pi = subprocess.Popen(options, shell=True, stdout=subprocess.PIPE)

    for i in iter(pi.stdout.readline, 'b'):
        re = i.decode().strip()
        if re == "":
            break
        try:
            hz = re.split(".")[-1]
            ml = re.split("/")[-2]
            if hz not in black_suffix:
                if ml not in black_list:
                    if re not in data:
                        data.append(re)
                        sub = re.split(" ")[0]
                        if sub in ('POST', 'GET'):
                            url = re.split(" ")[1]
                            req(sub, url)
        except IndexError:
            pass


def banner():
    print(r"""               _                     
 _ __ __ _  __| |___  ___ __ _ _ __  
| '__/ _` |/ _` / __|/ __/ _` | '_ \ 
| | | (_| | (_| \__ \ (_| (_| | | | |
|_|  \__,_|\__,_|___/\___\__,_|_| |_|
                          by:ifory  
""")


if __name__ == '__main__':
    banner()
    try:
        parameter = sys.argv[1]
        if parameter == "-u":
            target = sys.argv[2]
            run(target)
        elif parameter == "-f":
            with open(f"{sys.argv[2]}", 'r', encoding='utf-8') as f:
                for key in f.readlines():
                    target = key.strip()
                    run(target)
        else:
            print("Help: -u 目标URL\n      -f  从文件中导入目标URL批量查询\n")
    except IndexError:
        print("Help: -u 目标URL\n      -f 从文件中导入目标URL批量查询")
