爬取北京空气质量网站数据(加密的silverlight)
======

在网络良好的条件下, 可自动向北京空气质量网站请求数据, 进行解密和处理, 生成 (时间).txt 和 (时间).csv 两个文件, 分别保存空气质量数据的原始格式和表格格式.

如果需要定时执行, 可以直接使用Windows的计划任务.


# Dependency

- Windows OS (Win 7/10 tested)
- Python
- IronPython
- .Net Framework (>=4.5)

如果只是运行程序, 以上环境配置好后, 直接执行 bin/Release 文件夹下的 "aqi_crawler.exe" 程序.

- VS 2012 (编译环境)