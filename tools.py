import os
import re
import sys
import time

import gridfs
import pymongo
from selenium import webdriver


def improve_url(url) -> str:
    """
    improve_url 优化url格式为以"https://"开头且不以"/"结尾

    Args:
        url (str): 输入的url字符串，只优化以"//"开头或"/"结尾的url

    Returns:
        str: 优化后的url
    """
    if url.endswith('/'):
        url = url[:-1]
    if url.startswith('//'):
        url = 'https:' + url
    return url


class Logger(object):
    """
     日志类
    """

    def __init__(self, filepath="./logs/", filename="Default.log", stream=sys.stdout) -> None:
        self.terminal = stream
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        self.log = open(filepath+filename, "a")

    def write(self, message) -> None:
        self.terminal.write(message)
        self.log.write(message)

    def flush(self) -> None:
        pass


class Edgedriver:
    """
     基于selenium.webdriver的Edgedriver类

     默认无头模式及禁用gpu加速. 默认驱动器只对危害性错误进行log记录
    """
    # msedgedriver.exe的绝对路径
    executable_path = "D:/Anaconda/webdriver/edgedriver_win64/103.0.1264.62/msedgedriver.exe"

    def __init__(self, option=["--headless", "--disable-gpu", "--log-level=3"]) -> None:
        """
        Args:
            option (list, optional): 启动系数. Defaults to ["--headless", "--disable-gpu", "--log-level=3"].
        """
        self.option = option

    def run(self) -> webdriver.Edge:
        """
        run 启动驱动器

        通过修改webdriver.Edge的capabilities属性来添加启动系数
        """
        return webdriver.Edge(
            executable_path=self.executable_path,
            capabilities={
                "browserName": "MicrosoftEdge",
                "version": "",
                "platform": "WINDOWS",
                "ms:edgeOptions": {
                            "extensions": [],
                            "args": self.option,
                }
            })


class Snapshot:
    """
     进行全页面快照的类

     如需修改快照存放路径请前往line22上下寻找dirspath属性
    """

    def __init__(self, website, url, metadatabase='snapshot') -> None:
        """
        Args:
            website (str): 基站链接
            url (str): 需要进行快照的网页链接
            metadatabase (str): 存储快照的数据库名
        """
        self.website = website
        self.url = url
        self.metadatabase = metadatabase

    def shot(self) -> str:
        """
        shot 进行快照，并返回相应的反馈信息

        Returns:
            str: 反馈信息
        """
        # 启动驱动器并静态加载网页
        driver = Edgedriver().run()
        driver.get(self.url)
        while True:
            # 尝试点击式动态加载网页，针对https://news.youth.cn/
            try:
                # 根据class属性值找到'加载更多'的按钮
                button = driver.find_element_by_class_name("jzgd")
                # 驱动器循环点击按钮，每次点击后休整0.5(s)
                button.click()
                time.sleep(0.5)
            except Exception:
                # 找不到'加载更多'按钮后退出循环
                break
        # 用js获取页面的最大宽高
        scroll_width = driver.execute_script(
            "return document.body.parentNode.scrollWidth")
        scroll_height = driver.execute_script(
            "return document.body.parentNode.scrollHeight")
        # 将驱动器的宽高设置成刚刚获取的宽高，并等待2(s)使页面加载完全
        driver.set_window_size(
            width=scroll_width, height=scroll_height)
        time.sleep(2)
        # 获取此刻格式化后的时间
        # time.time():获取此刻时间戳
        # time.localtime():格式化时间戳为struct_time格式
        # time.strfttime():自定义时间格式
        current_time = time.strftime(
            '%Y%m%d%H%M%S', time.localtime(time.time()))
        # 拍摄全页面快照，基于current_time进行文件的命名
        data = driver.get_screenshot_as_png()
        driver.quit()
        # 通过正则匹配及字符串的split方法，由self.website生成合理的表名
        collection = re.sub(r'[\*:/\\\?\[\]<>\s*\.]', '_',
                            self.website.split("//")[-1])
        # 导入数据库，并分配数据存储位置
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        # 进入(创建)相应的数据库
        db = client[self.metadatabase]
        # 进入(创建)相应的容器
        fs = gridfs.GridFS(db, collection=collection)
        dic = {}
        dic['snapshot time'] = current_time
        dic['website url'] = self.url
        fs.put(data, **dic)
        # os.getpid(): 获取当前进程的进程ID
        print(str(self.url) +
              " :Process {} get snapshot !".format(os.getpid()))
        # 将current_time作为反馈信息进行返回
        return current_time
