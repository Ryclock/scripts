# 多线程持续型图片爬虫{ignore=true}

这是一个多线程持续型图片爬虫，用于每两小时爬取指定网站及其直接关联的网页的页面图片，并将图片存储于本地 MongoDB 数据库中。请注意，该爬虫并不具有广泛适用性，仅适用于特定的爬取任务。

## 目录
[TOC]
  
## 切换语言

- [English](./README_en.md)

## 开发环境


| 库名        | 版本号        | 备注                 |
| ----------- | ------------- | -------------------- |
| Vscode      | 1.63          | 编辑器               |
| conda       | 4.13.0        | 软件包和环境管理系统 |
| python      | 3.9.7         | 编程语言             |
| bs4         | 4.10.0        | Python 第三方库      |
| requests    | 2.27.1        | Python 第三方库      |
| selenium    | 3.141.0       | Python 第三方库      |
| pymongo     | 3.12.0        | Python 第三方库      |
| apscheduler | 3.7.0         | Python 第三方库      |
| Edge        | 103.0.1264.62 | 浏览器               |
| msedgedrive | 103.0.1264.62 | 驱动器               |
| MongoDB     | 5.0.9         | 数据库               |

## 版本更迭


| 版本号 | 更新时间         | 备注                                                                                                                                                                                                                                                                                                                                             |
| ------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.1.0  | 2022.7.14 20:11  | 实现静态爬取，爬取对象：[中青网](https://www.youth.cn/)                                                                                                                                                                                                                                                                                          |
| 1.2.0  | 2022.7.15 20:32  | 解决全页面快照；实现点击型动态爬取，爬取对象：[中青网（新闻专题）](https://news.youth.cn/)                                                                                                                                                                                                                                                       |
| 1.2.1  | 2022.7.16 00:12  | 修复漏洞；完成注释的编写                                                                                                                                                                                                                                                                                                                         |
| 1.2.2  | 2022.7.16 12:10  | 模块化现有代码，修复漏洞                                                                                                                                                                                                                                                                                                                         |
| 1.2.3  | 2022.7.16 16:23  | tools 模块新增 improve_dirspath 方法，删除 spiders 模块 Spider_imgs 类的 __get_dirspath 方法；修改 tools 模块的 improve_url 及 improve_picurl 方法；tools 模块新增 init_buffertxt 方法；修改 spiders 模块 Spider_imgs 类的 __save_img 方法为 save_img 方法，此方法新增对 base64 编码图片的解码保存功能                                           |
| 1.3.0  | 2022.7.17 00:10  | 实现小规模持续性爬取，拓展爬取对象：[中青网（新闻专题）](https://news.youth.cn/)[中国网](http://www.china.com.cn/)[腾讯网](https://www.qq.com/)[光明网](https://www.gmw.cn/)，修复漏洞                                                                                                                                                           |
| 1.3.1  | 2022.7.17 11:04  | 解决 base64 编码链接存储问题；优化逻辑：先获取图片 URL 并进行去重后才进行快照拍摄                                                                                                                                                                                                                                                                |
| 1.3.2  | 2022.7.17 12:21  | tools 模块新增 Logger 类，用于保存与终端输出一致的日志文件；修改元数据列表："爬取耗时/秒" -> "本地图片大小"；修改了本地存储路径的文件树                                                                                                                                                                                                          |
| 1.4.0  | 2022.7.17 19:32  | 修改元数据记录方式为获取后直接记录，重构 spiders 模块中 Spider_imgs 类的 get_datalist 方法和 save_metaData 方法 -> check_sheet 方法和新的 save_metaData 方法；优化元数据列表：'本地存储'单元格新增'此程序不支持这种链接格式'提示文本；优化本地存储路径；tools 模块新增 excel_is_active 方法，spiders 模块 Spider_links 类中新增 check_sheet 方法 |
| 1.4.1  | 2022.7.17 21:43  | 决定不爬取政府网站，修改 spiders 模块的 Spider_links 类中的 ask_url 方法，实现下拉型动态爬取，如[QQ新闻（教育板块）](https://new.qq.com/ch/edu/)；修复漏洞                                                                                                                                                                                       |
| 1.4.2  | 20222.7.18 08:59 | 修改为使用 BackgroundScheduler 类，进行后台立即启动的周期性持续爬取；修复漏洞                                                                                                                                                                                                                                                                    |
| 1.4.3  | 2022.7.18 13:10  | 实现小规模多线程爬取图片，新增过程锁；分离图片下载和元数据存储；修复漏洞                                                                                                                                                                                                                                                                         |
| 1.4.4  | 2022.7.18 16:01  | 采用 MongoDB 代替 Excel 存储元数据                                                                                                                                                                                                                                                                                                               |
| 1.5.0  | 2022.7.19 23:06  | 采用 MongoDB 代替文件系统存储目标图片，修复漏洞                                                                                                                                                                                                                                                                                                  |
| 1.5.1  | 2022.7.20 13:41  | 采用 MongoDB 代替文件系统存储快照图片(快照图片和目标图片均以二进制形式使用 gridfs 模块进行存储)，删除 tools 模块多余的函数方法                                                                                                                                                                                                                   |

## 参考网站

- [pymongo使用BSON类型存取(图片)文件](https://blog.csdn.net/lpwmm/article/details/105377303)
- [Logger类](https://blog.csdn.net/qq_39564555/article/details/112135970)
- [异步+多进程](https://blog.csdn.net/SL_World/article/details/86633611)
- [apscheduler CSDN](https://blog.csdn.net/abc_soul/article/details/88875643)
- [apscheduler API](https://apscheduler.readthedocs.io/en/latest/modules/triggers/combining.html#module-apscheduler.triggers.combining)
- [Chrome浏览器启动参数](https://www.cnblogs.com/gurenyumao/p/14721035.html)
- [文件目录树](https://blog.csdn.net/SilenceJude/article/details/99673949)
- [bs4库](http://c.biancheng.net/python_spider/bs4.html)
- [Requests库](https://www.w3cschool.cn/requests2/requests2-r81j3fjc.html)
- [快照](https://blog.csdn.net/qq_45030271/article/details/114760346)
- [Re库](https://docs.python.org/zh-cn/3/library/re.html)
