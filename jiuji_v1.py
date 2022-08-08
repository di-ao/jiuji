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
#url表
URL_LIST_PORT = []
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
        # print("未知错误:%s"% result)
        pass


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
        # print("未知错误:%s"% result)
        pass


def re():
    """检测主模块"""


    url_https = "https://"
    url_http = "http://"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    proxies = {"http": PROXY}
    port = ["80", "443", "4443", "21", "2121", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "7001", "7002", "8000", "8088", "8080", "8081", "8089", "8161", "8443", "8880", "8888", "9001", "9090", "9080", "5800", "5443", "5984", "9200", "9300", "10000", "28017", "50070", "2181", "9092", "16010", "60010", "1900"]
    
    with open("domain2.txt") as domian:
        domain_list = domian.readlines()
        
        if not domain_list:
            print("domain2.txt文件没有内容,请重新尝试")
            sys.exit()
        else:
            for d in domain_list:
                for p in port:
                    url_list1 = url_http + d.strip() + ":" + p
                    url_list2 = url_https + d.strip() + ":"  + p
                    URL_LIST_PORT.append(url_list1)
                    URL_LIST_PORT.append(url_list2)
                    
            
            with ThreadPoolExecutor(max_workers=500) as t:
                if len(PROXY) > 0:
                    print("**检测使用代理** 正在检测请稍等...")
                    for line in URL_LIST_PORT:
                        t.submit(re_proxy, line, headers, proxies)
              
                else:
                    print("**检测未使用代理** 正在检测请稍等...")
                    for line in URL_LIST_PORT:
                        t.submit(re_not, line, headers)
            print("**检测完成**")
    URL_LIST_PORT.clear()
    url = list(set(URL_LIST))
    with open("url.txt","w") as url_list3: 
        for i in url:
            url_list3.write(f"{i}\n")
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
        rad_lists = rad_url.readlines()
        if not rad_lists:
            print("url.txt文件没有内容,请重新尝试")
            sys.exit()
        else:    
            lines = list(set(rad_lists))
            for line in lines:
                url = line.strip()
                cmd = subprocess.Popen([RAD, '-t', url, '--http-proxy', '127.0.0.1:7777'], shell=True, encoding="utf-8",cwd=RAD_PHAT)
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
                        
                    【啾乩】-Ver1.1                                                 
                1.子域名爆破+批量存活检测
                2.Ehole + observer 批量指纹识别
                3.rad批量爬虫
                4.使用所有功能

    """)

    num = input("请输入对应功能的数字:")
    if num == "1":
        # while True:
            
        print("""
        1.子域名爆破
        2.IP/域名批量存活检测
        3.子域名爆破+批量存活检测
        """)
        num1 = input("请输入对应功能的数字:")
        if num1 == "1":
            domian()
            # sys.exit()
        elif num1 == "2":
            re()
            # sys.exit()
        elif num1 == "3":
            domian()
            re()
            # sys.exit()
        else:
            print("输入错误,请重新输入!")
            # cmd = subprocess.Popen('cls', shell=True)
                # cmd.wait()
            sys.exit()

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
