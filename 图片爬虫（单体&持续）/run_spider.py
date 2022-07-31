import sys
import time

import tools
from spiders import Spider_links


def run_spider(website, metadatabase):
    """
    run_spider 爬虫运行程序

    Args:
        website (str): 基站链接
        metadatabase (str): 数据库名
    """
    # 日志文件名按照程序运行时间设置
    filename = time.strftime(
        "%Y%m%d", time.localtime()) + '.log'
    # 记录正常的 print 信息
    sys.stdout = tools.Logger(filename=filename)
    # 记录 traceback 异常信息
    sys.stderr = tools.Logger(filename=filename)
    print('\n\r'+time.asctime(time.localtime(time.time())) +
          ": start spider, website "+website)
    spider = Spider_links(website, metadatabase)
    spider.run()
    print(time.asctime(time.localtime(time.time())) +
          ": finish spider, website "+website)
    sys.stdout = tools.Logger(filename=filename)
    # 记录 traceback 异常信息
    sys.stderr = tools.Logger(filename=filename)
    time.sleep(120)
