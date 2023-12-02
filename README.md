# xray_html_to_xlsx
**Convert xray HTML report files to xlsx files for data organization**

```python
#代码释义
1.设置全局目录变量，并判断全局目录是否存在，若不存在即创建；
2.遍历xray_report_dir目录下所有html文件；
3.读取遍历的所有html文件内容；
4.re正则匹配漏洞信息大致范围；
5.再利用正则匹配单个关键字数据（create_time、target、plug、extra）并将提取的create_time的时间戳转换成日期格式；
6.将所要填充的关键字数据添加到vuln_data列表当中；
7.创建数据框架，并将vuln_data列表中数据填充对应自定义列字段值下；
8.判断file_path目录下是否存在备份文件 *.bak；否则直接移除；
9.判断要写入的excel文件是否存在，若存在即重命名 *.bak后再写入excel文件中；否则直接写入；

#!!!注意将要整理的xray扫描的html报告放入xray_report_dir下，直接运行即可
python xray_html_to_xlsx.py
```

![](.\example.png)
