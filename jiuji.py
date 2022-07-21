import sys
import subprocess
import shutil
import urllib3
import requests
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings()
# 工具路径及工作目录配置(必须为绝对路径,请使用/分割目录,补充前面xxx目录即可)
KSUBDOMAIN = "xxx/ksubdomain/ksubdomain.exe" 
KSUBDOMAIN_PHAT = "xxx/ksubdomain/"
EHOLE = "xxx/Ehole/Ehole3.0-Win.exe"
EHOLE_PHAT = "xxx/Ehole/"
OBSERVER = "xxx/observer/observer_ward.exe"
OBSERVER_PHAT = "xxx/observer/"
RAD = "xxx/rad/rad_windows_amd64.exe"
RAD_PHAT = "xxx/rad/"
# url检测代理,只支持http,例:http://127.0.0.1:10809
PROXY = ""
URL_LIST = []
def domian():
    """ksubdomain"""
    
    
    shutil.copyfile("domain.txt", KSUBDOMAIN_PHAT + "domain.txt")

    # cmd = subprocess.Popen([KSUBDOMAIN, 'e', '--dl', 'domain.txt', '--od', '-o', 'domian2.txt'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", cwd=KSUBDOMAIN_PHAT)
    cmd = subprocess.Popen([KSUBDOMAIN, 'e', '--dl', 'domain.txt', '-b', '5m', '--od', '-o', 'domain2.txt'], shell=True, encoding="utf-8", cwd=KSUBDOMAIN_PHAT)
    cmd.wait()
    print("\n")
    # if cmd.poll() == 0:
    #     print(cmd.communicate())
    # else:
    #     print("失败")
    
    shutil.move(KSUBDOMAIN_PHAT + "domain2.txt", "domain2.txt")


def re_proxy(url, headers, proxies):
    """使用代理检测"""
    
    try:
        r1 = requests.get(url, headers=headers,proxies=proxies, timeout=(3, 9), verify=False)
        if r1.status_code == requests.codes.ok:
            URL_LIST.append(r1.url)
            
    # except requests.exceptions.ReadTimeout:
    #     print("代理连接超时")                
    # except requests.exceptions.ProxyError:
    #     print("代理连接不上")
    except Exception as result:
        print("未知错误:%s"% result)


def re_not(url, headers):
    """不使用代理检测"""

    try:
        r2 = requests.get(url, headers=headers, timeout=(3, 9), verify=False)
        if r2.status_code == requests.codes.ok:
            URL_LIST.append(r2.url)
            
    # except requests.exceptions.ReadTimeout:
    #     print("代理连接超时")                
    # except requests.exceptions.ProxyError:
    #     print("代理连接不上")
    except Exception as result:
        print("未知错误:%s"% result)


def re():
    """检测主模块"""
    url_https = "https://"
    url_http = "http://"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    proxies = {"http": PROXY}
    
    with open("domain2.txt") as domian:
        domain_list = domian.readlines()
        
        if not domain_list:
            print("domain2.txt文件没有内容,请重新尝试")
            sys.exit()
        else:
            with ThreadPoolExecutor(1000) as t:
                if len(PROXY) > 0:
                    print("检测使用代理!")
                    for line in domain_list:
                        t.submit(re_proxy, url_http+line.strip(), headers, proxies)
                        t.submit(re_proxy, url_https+line.strip(), headers, proxies)
                else:
                    print("检测未使用代理!")
                    for line in domain_list:
                        t.submit(re_not, url_http+line.strip(), headers)
                        t.submit(re_not, url_https+line.strip(), headers)
    url = list(set(URL_LIST))
    with open("url.txt","w") as url_list2: 
        for i in url:
            url_list2.write(f"{i}\n")
    URL_LIST.clear()
    
        
def ehole():
    """Ehole"""


    shutil.copyfile("url.txt", EHOLE_PHAT + "url.txt")

    cmd = subprocess.Popen([EHOLE, '-l', 'url.txt', '-json', 'ehole.json'], shell=True, encoding="utf-8", cwd=EHOLE_PHAT)
    cmd.wait()
   
    shutil.move(EHOLE_PHAT + "ehole.json", "ehole.json")


def observer():
    """observer"""


    shutil.copyfile("url.txt", OBSERVER_PHAT + "url.txt")
    
    if len(PROXY) > 0:
        cmd = subprocess.Popen([OBSERVER, '-f', 'url.txt', '-c', 'observer.csv', '--proxy', PROXY], shell=True, encoding="utf-8", cwd=OBSERVER_PHAT)      
        cmd.wait()
    else:
        print("observer未使用代理!")
        cmd = subprocess.Popen([OBSERVER, '-f', 'url.txt', '-c', 'observer.csv'], shell=True, encoding="utf-8", cwd=OBSERVER_PHAT)      
        cmd.wait()

    shutil.move(OBSERVER_PHAT + "observer.csv", "observer.csv")


def rad():
    """rad爬虫"""

    
    with open("url.txt") as rad_url:
        rad_list = rad_url.readlines()
        if not rad_list:
            print("url.txt文件没有内容,请重新尝试")
            sys.exit()
        else:    
            for lines in rad_list:
                line = lines.strip()
                cmd = subprocess.Popen([RAD, '-t', line, '--http-proxy', '127.0.0.1:7777'], shell=True, encoding="utf-8",cwd=RAD_PHAT)
                cmd.wait()


def all():
    domian()
    re()
    ehole()
    observer()
    rad()


if __name__ == "__main__":
    print("""
  ________    _____   __    __    ________    _____  
 (___  ___)  (_   _)  ) )  ( (   (___  ___)  (_   _) 
     ) )       | |   ( (    ) )      ) )       | |   
    ( (        | |    ) )  ( (      ( (        | |   
 __  ) )       | |   ( (    ) )  __  ) )       | |   
( (_/ /       _| |__  ) \__/ (  ( (_/ /       _| |__ 
 \___/       /_____(  \______/   \___/       /_____( 
                        
                        【啾乩】                                                 
                1.子域名爆破+批量存活检测
                2.Ehole + observer 批量指纹识别
                3.rad批量爬虫
                4.使用所有功能

    """)

    num = input("请输入对应功能的数字:")
    if num == "1":
        domian()
        re()
    elif num == "2":
        ehole()
        observer()  
    elif num == "3":
        rad()
    elif num  == "4":
        all()
    else:
        print("输入错误,请重新输入!")
        sys.exit()