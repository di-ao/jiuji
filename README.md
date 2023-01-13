# 啾乩简介：

一个小轱辘，调用常用工具帮助红队快速自动化打点。

功能：子域名爆破+存活检测，资产指纹批量识别，url批量爬虫+漏洞扫描。

开发环境：python3.8

------

# 缝合工具

| 工具名称                                                 | 功能         |
| -------------------------------------------------------- | ------------ |
| [**Ksubdomain**](https://github.com/boy-hack/ksubdomain) | 子域名爆破   |
| [**Observer**](https://github.com/0x727/ObserverWard)    | 资产指纹识别 |
| [**Ehole**](https://github.com/EdgeSecurityTeam/EHole)   | 资产指纹识别 |
| [**Rad**](https://github.com/chaitin/rad)                | 网络爬虫     |
| [**Xray**](https://github.com/chaitin/xray)              | 漏洞扫描     |

------

# 计划更新

- [x] 添加web常用端口检测

- [ ] 添加主机扫描模块

------

# 快速使用

## 1.整体执行流程

![](https://github.com/di-ao/jiuji/blob/main/img/%E6%B5%81%E7%A8%8B.png)

------

## 2.使用

1. 安装requests和urllib3库。

   ```
   pip install requests
   pip install urllib3
   ```

2. 根据自己电脑环境更改jiuji.py脚本里面的工具路径及工具目录。

   <img src="https://github.com/di-ao/jiuji/blob/main/img/%E8%B7%AF%E5%BE%84.png" />

3. 添加域名到domain.txt -->（域名爆破） ||  添加IP/域名到domain2.txt -->（存活检测） ||  添加url到url.txt --> （指纹识别&爬虫）【每行一个域名/IP】

4. 使用功能模块。

   > - 如果使用3、4功能模块，必须先启动xray！！！
   >
   > - **强烈建议xray和rad根据实际环境需求更改config配置文件**。

   ```
   xray.exe webscan --listen 127.0.0.1:7777 --html-output xxx.html
   ```

   - 注意:此模块批量存活检测默认不检测web常用端口！！！需要启用请在all()函数内的re()函数设置为re(True)
   
   <img src="https://github.com/di-ao/jiuji/blob/main/img/%E5%8A%9F%E8%83%BD.png" />

------

## 3.注意事项

- observe导出csv文件查看乱码，可使用notepad++，选择【编码】-【转为ANSI编码】
- rad需要安装**chrome**浏览器（在windows平台可调用win10自带edge浏览器，不一定需要安装**chrome**）
- IP/域名批量存活检测模块默认线程池的值500，可根据需求设置。检测速度受电脑性能、线程池值和上游代理影响。

------

# iヾ(•ω•`)o

- **感谢缝合工具项目组的所有成员！！！**

- 感兴趣的请合理使用，遵纪守法！！！

  

