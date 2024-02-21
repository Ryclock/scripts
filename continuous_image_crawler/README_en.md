# Multi-threaded Continuous Image Crawler{ignore=true}

This crawler is designed to scrape images from a website and its directly associated web pages every two hours. The scraped images are stored in a local MongoDB database. Please note that this crawler is not intended for general-purpose use.

## Table
[TOC]

## something else

- There are many loopholes and shortcomings in the project, and there are no plans to continue optimizing it.
- [中文](./README.md)

## Possible Configuration Requirements

| Library     | Version       | Remarks                                            |
| ----------- | ------------- | -------------------------------------------------- |
| Vscode      | 1.63          | Editor                                             |
| conda       | 4.13.0        | Software package and environment management system |
| python      | 3.9.7         | Programming language                               |
| bs4         | 4.10.0        | Python third-party library                         |
| requests    | 2.27.1        | Python third-party library                         |
| selenium    | 3.141.0       | Python third-party library                         |
| pymongo     | 3.12.0        | Python third-party library                         |
| apscheduler | 3.7.0         | Python third-party library                         |
| Edge        | 103.0.1264.62 | Browser                                            |
| msedgedrive | 103.0.1264.62 | Driver                                             |
| MongoDB     | 5.0.9         | Database                                           |

## Version History

| Version | Release Date | Remarks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.1.0   | 2022-07-14   | Implemented static crawling, targeted website: [Youth.cn](https://www.youth.cn/)                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 1.2.0   | 2022-07-15   | Resolved full-page snapshot issue; implemented dynamic crawling with click actions, targeted website: [Youth.cn News Special](https://news.youth.cn/)                                                                                                                                                                                                                                                                                                                                            |
| 1.2.1   | 2022-07-16   | Bug fixes; completed code comments                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 1.2.2   | 2022-07-16   | Modularized existing code; fixed bugs                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 1.2.3   | 2022-07-16   | Added the `improve_dirspath` method to the `tools` module, removed the `__get_dirspath` method from the `Spider_imgs` class in the `spiders` module; modified the `improve_url` and `improve_picurl` methods in the `tools` module; added the `init_buffertxt` method to the `tools` module; modified the `save_img` method in the `Spider_imgs` class to support saving base64-encoded images                                                                                                   |
| 1.3.0   | 2022-07-17   | Implemented small-scale continuous crawling, expanded target websites: [Youth.cn News Special](https://news.youth.cn/), [China.com.cn](http://www.china.com.cn/), [Tencent News](https://www.qq.com/), [Guangming News](https://www.gmw.cn/); fixed bugs                                                                                                                                                                                                                                         |
| 1.3.1   | 2022-07-17   | Resolved base64-encoded link storage issue; optimized logic to first retrieve image URLs and remove duplicates before taking snapshots                                                                                                                                                                                                                                                                                                                                                           |
| 1.3.2   | 2022-07-17   | Added `Logger` class to save log files consistent with terminal output; modified metadata list: changed "Crawling Time/seconds" to "Local Image Size"; modified local storage directory structure                                                                                                                                                                                                                                                                                                |
| 1.4.0   | 2022-07-17   | Changed metadata recording method to directly record after retrieval; refactored `get_datalist` and `save_metaData` methods in the `Spider_imgs` class to `check_sheet` and the new `save_metaData` method; optimized metadata list: added "This program does not support this link format" text to the "Local Storage" cell; optimized local storage path; added `excel_is_active` method to the `tools` module, added `check_sheet` method to the `Spider_links` class in the `spiders` module |
| 1.4.1   | 2022-07-17   | Removed government websites from crawling targets; modified the `ask_url` method in the `Spider_links` class to implement dynamic crawling with dropdown menus, e.g., [QQ News (Education Section)](https://new.qq.com/ch/edu/); fixed bugs                                                                                                                                                                                                                                                      |
| 1.4.2   | 2022-07-18   | Switched to using `BackgroundScheduler` for background immediate start periodic crawling; fixed bugs                                                                                                                                                                                                                                                                                                                                                                                             |
| 1.4.3   | 2022-07-18   | Implemented small-scale multi-threaded image crawling; added process lock; separated image downloading and metadata storage; fixed bugs                                                                                                                                                                                                                                                                                                                                                          |
| 1.4.4   | 2022-07-18   | Replaced Excel storage with MongoDB for metadata storage                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 1.5.0   | 2022-07-19   | Replaced file system storage with MongoDB for target images; fixed bugs; fixed the issue of losing the last log entry (to be improved)                                                                                                                                                                                                                                                                                                                                                           |
| 1.5.1   | 2022-07-20   | Replaced file system storage with MongoDB for snapshot images (both snapshot and target images are stored as binary data using the `gridfs` module); removed unnecessary functions from the `tools` module                                                                                                                                                                                                                                                                                       |

## References

- [Using BSON Type to Store/Retrieve (Image) Files with pymongo](https://blog.csdn.net/lpwmm/article/details/105377303)
- [Logger Class](https://blog.csdn.net/qq_39564555/article/details/112135970)
- [Asynchronous + Multiprocessing](https://blog.csdn.net/SL_World/article/details/86633611)
- [apscheduler CSDN](https://blog.csdn.net/abc_soul/article/details/88875643)
- [apscheduler API](https://apscheduler.readthedocs.io/en/latest/modules/triggers/combining.html#module-apscheduler.triggers.combining)
- [Chrome Browser Startup Parameters](https://www.cnblogs.com/gurenyumao/p/14721035.html)
- [File Directory Tree](https://blog.csdn.net/SilenceJude/article/details/99673949)
- [bs4 Library](http://c.biancheng.net/python_spider/bs4.html)
- [Requests Library](https://www.w3cschool.cn/requests2/requests2-r81j3fjc.html)
- [Snapshot](https://blog.csdn.net/qq_45030271/article/details/114760346)
- [re Library](https://docs.python.org/zh-cn/3/library/re.html)
