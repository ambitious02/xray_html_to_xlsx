# -*- coding: utf-8 -*-
# @Author  : aysec
# @Time    : 12/2/2023 17:30 PM
# @Describe: Convert xray HTML report files to xlsx files for data organization

'''
!!!注意将要整理的xray扫描的html报告放入xray_report_dir下，直接运行即可
1.设置全局目录变量，并判断全局目录是否存在，若不存在即创建；
2.遍历xray_report_dir目录下所有html文件；
3.读取遍历的所有html文件内容；
4.re正则匹配漏洞信息大致范围；
5.再利用正则匹配单个关键字数据（create_time、target、plug、extra）并将提取的create_time的时间戳转换成日期格式；
6.将所要填充的关键字数据添加到vuln_data列表当中；
7.创建数据框架，并将vuln_data列表中数据填充对应自定义列字段值下；
8.判断file_path目录下是否存在备份文件 *.bak；否则直接移除；
9.判断要写入的excel文件是否存在，若存在即重命名 *.bak后再写入excel文件中；否则直接写入；
'''

import re
import os
import glob
import datetime
import pandas as pd

#1.设置全局目录变量，并判断全局目录是否存在，若不存在即创建；
#指定目标目录
file_path = 'result'
#指定xray扫描结果html文件目录
xray_report_dir = 'xray_report_dir'
#漏洞数据列表
vuln_data = []
#判断目录是否存在，不存在则创建
if not os.path.exists(file_path):
    os.mkdir(file_path)
if not os.path.exists(xray_report_dir):
     os.mkdir(xray_report_dir)

#2.遍历xray_report_dir目录下所有html文件；
#使用glob模块匹配目录下的所有HTML文件
html_files = glob.glob(os.path.join(xray_report_dir, '*.html'))
#
# 遍历文件列表并进行处理
for html_file in html_files:
    #获取HTML文件的文件名（不包括扩展名）
    file_name = os.path.splitext(os.path.basename(html_file))[0]
    #print(file_name)
    #使用文件路径+遍历的所有文件名+html后缀
    file = os.path.join(xray_report_dir,file_name + '.html')
    #print(file)

    #3.读取遍历的所有html文件内容；
    #遍历读取当前目录所有html文件内容
    with open(file ,'r', encoding='utf-8') as f:
        print("读取文件："+file)
        html = f.read()

        #4.re正则匹配漏洞信息大致范围；
        #使用正则表达式提取漏洞信息
        vuln_info = re.findall(r"<script class='web-vulns'>webVulns.push\((.*?)\)</script>", html, re.M | re.I)

        #5.再利用正则匹配单个关键字数据（create_time、target、plug、extra）并将提取的create_time的时间戳转换成日期格式；
        #使用正则表达式提取漏洞信息
        for info in vuln_info:
            #提取时间戳
            create_time = re.search(r'create_time":(\d+)', info).group(1)
            #将时间戳转换为日期
            timestamp = int(create_time)
            date = datetime.datetime.fromtimestamp(timestamp / 1000.0)  # 注意这里需要除以1000，因为时间戳通常是以秒为单位的
            #提取插件
            plugin = re.search(r'plugin":"([^"]+)"', info).group(1)
            #提取目标
            target = re.search(r'target":{"url":"([^"]+)"', info).group(1)
            #提取关键字
            extra = re.search(r'extra":({[^}]+})', info).group(1)

            #6.将所要填充的关键字数据添加到vuln_data列表当中；
            vuln_data.append({'create_time': date, 'target': target, 'PluginName/VulnType': plugin, 'Extra': extra})
#print(vuln_data)

#7.创建数据框架，并将vuln_data列表中数据填充对应自定义列字段值下；
#创建DataFrame
df = pd.DataFrame(vuln_data, columns=['create_time', 'target', 'PluginName/VulnType', 'Extra'])

#8.判断file_path目录下是否存在备份文件 *.bak；否则直接移除；
#判断备份文件是否存在
if os.path.exists(file_path+'/xray_vulnerabilities.xlsx.bak'):
    os.remove(file_path+'/xray_vulnerabilities.xlsx.bak')

#9.判断要写入的excel文件是否存在，若存在即重命名 *.bak后再写入excel文件中；否则直接写入；
#判断文件是否存在
if os.path.exists(file_path+'/xray_vulnerabilities.xlsx'):
    #存在就重命名
    os.renames(file_path+'/xray_vulnerabilities.xlsx',file_path+'/xray_vulnerabilities.xlsx.bak')
    #将数据写入Excel文件
    df.to_excel(file_path+'/xray_vulnerabilities.xlsx', index=False)
else:
    #将数据写入Excel文件
    df.to_excel(file_path+'/xray_vulnerabilities.xlsx', index=False)