import base64
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import bs4
import gridfs
import pymongo
import requests
from PIL import Image

import tools


def ask_url(url) -> bs4.BeautifulSoup:
    """
    ask_url 对url发送访问请求，访问成功返回对应的bs4.BeautifulSoup对象. 访问失败抛出异常，并在终端提示

    Raises:
        e: 出现链接无效情况
        Exception: 不爬政府网站

    Returns:
        bs4.BeautifulSoup: 使用"html.parser"解析后的bs4.BeautifulSoup对象
    """
    # 启动驱动器并静态加载网页
    try:
        if '.gov.cn' in url:
            print(url + ' :government website !!!')
            raise Exception()
        driver = tools.Edgedriver().run()
        driver.get(url)
    except Exception as e:
        print(url+' :connect Wrong !!!')
        driver.quit()
        raise e
    else:
        # 尝试动态加载网页（点击型），针对https://news.youth.cn/，最多点击10次
        i = 1
        while True:
            try:
                # 根据class属性值找到'加载更多'的按钮
                button = driver.find_element_by_class_name("jzgd")
                # 驱动器循环点击按钮，每次点击后休整0.5(s)
                button.click()
                i += 1
                time.sleep(2)
                if i == 11:
                    break
            except Exception:
                # 找不到'加载更多'按钮后退出循环
                break
        pre_height = []
        # 存储当前页面的最大高度
        pre_height.append(driver.execute_script(
            "return document.body.scrollHeight;"))
        # 尝试动态加载网页（下拉刷新型），最多下拉10次
        while True:
            # 驱动器执行下拉滚动条操作
            driver.execute_script("scroll(0,5000)")
            time.sleep(2)
            new_height = driver.execute_script(
                "return document.body.scrollHeight;")
            # 判断是否已经到底
            if new_height == pre_height[-1] or len(pre_height) == 11:
                break
            # 更新最大高度
            else:
                pre_height.append(new_height)
        # 解析网页，并关闭驱动器
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        print(url+' :connect !')
        return soup


class Spider_links:
    """
     用于爬取与website有直接关系的url，并通过调用Spider_imgs类将这些url上的图片群及其元数据保存到本地.

     目前url爬取范围仅限self.website本身及与其页面上直接提供的所有url
    """
    # url查找规则
    reg = r'<a.*href="(?P<target>[^.].*?)".*>'
    findLink = re.compile(reg, re.S)

    def __init__(self, website, metadatabase) -> None:
        """
        Args:
            website (str): 输入的网站首页
            metadatabase (str): 存储图片的数据库名
        """
        self.website = website
        self.metadatabase = metadatabase

    def run(self) -> None:
        """
        run Spider_links的main方法

        采用多线程爬取. 爬取开始和爬取成功结束时，均会在终端提示
        """
        linklist = self.get_linklist()
        print(str(self.website) +
              " :starts {}URL(total)".format(len(linklist)))
        # 采用多线程爬取链接列表的网页上的图片群，暂时只选择最大线程数为5
        with ThreadPoolExecutor(max_workers=5) as pool:
            for url in linklist:
                spider_imgs = Spider_imgs(self.website, url)
                pool.submit(spider_imgs.run)
            # 关闭线程池，等待全部任务完成
            pool.shutdown()

    def get_linklist(self) -> list:
        """
        get_linklist 获取url列表

        Returns:
            list: 至少有一个元素，即self.website本身
        """
        # 一维列表初始化为含有一个元素为self.website
        linklist = [self.website]
        for item in ask_url(self.website).find_all(name='a', recursive=True):
            # 匹配合法的url，并保存到变量raw中
            raw = re.fullmatch(pattern=self.findLink, string=str(item))
            if raw:
                # 若匹配成功，则向一维列表添加元素
                # 防止采用多分组的匹配规则，此处筛选出来目标分组(即url)
                linklist.append(tools.improve_url(raw.group('target')))
        # 对url列表进行无序去重
        linklist = list(set(linklist))
        return linklist


class Spider_imgs:
    """
     用于爬取指定网页的图片群并生成对应的元数据的单体爬虫
    """
    # 图片链接查找规则
    reg = r'<img.*\b(src|data-original)\b="(?P<target>[^.].*?)".*>'
    findImgSrc = re.compile(reg, re.S)
    # 简单的反反爬措施，应对图片链接
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    def __init__(self, website, url, metadatabase='src') -> None:
        """
        Args:
            website (str): 来源于Spider_links的网站首页
            url (str): 指定爬取的网页
            metadatabase (str): 存储图片的数据库名
        """
        self.website = website
        self.url = url
        self.metadatabase = metadatabase

    def run(self) -> None:
        """
        run Spider_imgs的main方法

        以快照的拍摄成功作为爬取成功的标志. 若成功完成爬取则在终端提示
        """
        # 日志文件名按照程序运行时间设置
        filename = time.strftime(
            "%Y%m%d", time.localtime()) + '.log'
        # 记录正常的 print 信息
        sys.stdout = tools.Logger(filename=filename)
        # 记录 traceback 异常信息
        sys.stderr = tools.Logger(filename=filename)
        try:
            self.save_metaData()
        except Exception:
            # 判断是否成功爬取的终端提示
            print(str(self.url) + " :Wrong!!!")
        else:
            print(self.url+" :finish !")

    def save_metaData(self) -> None:
        """
        save_metaData 爬取图片群，并保存其元数据

        Raises:
            e: 此方法不处理异常，仅将异常自下而上抛出
            Exception: 将url内无图片视为异常
        """
        try:
            soup = ask_url(self.url)
            # 遍历所有img标签，找到合适的picurls列表
            picurls = []
            for item in soup.find_all(name='img', recursive=True):
                # 匹配合法的图片链接，并保存到变量raw中
                raw = re.fullmatch(pattern=self.findImgSrc, string=str(item))
                if raw:
                    # 若匹配成功，则向picurls列表添加元素
                    # 防止采用多分组的匹配规则，此处筛选出来目标分组(即图片链接)
                    picurls.append(tools.improve_url(raw.group('target')))
            # picurls列表为空，则代表此url内无图片
            if not picurls:
                print(str(self.url) + " :no imgs !!!")
                raise Exception()
            # picurls列表去重
            picurls = list(set(picurls))
            # 全页面快照拍摄
            shot_info = tools.Snapshot(self.website, self.url).shot()
            # 通过正则匹配及字符串的split方法，由self.website生成合理的表名
            collection = re.sub(r'[\*:/\\\?\[\]<>\s*\.]', '_',
                                self.website.split("//")[-1])
            # 导入数据库，并分配数据存储位置
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            # 进入(创建)相应的数据库
            db = client[self.metadatabase]
            # 进入(创建)相应的容器
            fs = gridfs.GridFS(db, collection=collection)
            for picurl in picurls:
                picurl = picurl.replace('&amp;', '&')
                if picurl.startswith('data:image'):
                    # 切割字符串，获取后面图片数据部分
                    # 解码-->二进制数据
                    data = base64.b64decode(
                        bytes(picurl.split(',')[-1], 'utf-8'))
                else:
                    try:
                        response = requests.get(url=picurl,
                                                headers=self.headers,
                                                timeout=5)
                        if response.status_code != 200:
                            print(picurl+' :picurl connect Wrong !!!')
                            raise Exception()
                    except Exception:
                        # 以下异常情况均会被捕捉并在终端提示
                        # 暂时不支持对图片链接为相对路径的解析
                        # 请求超过5(s)则判断为图片链接网址加载失败(爬虫假死)
                        print(picurl+' :timeout or relative path !')
                    data = response.content
                # time.time():获取此刻时间戳
                # time.localtime():格式化时间戳为本地的时间
                # time.asctime(): 可读化时间，形如"Tue Dec 11 18:07:14 2008"
                crawling_time = time.asctime(time.localtime(time.time()))
                dic = {}
                dic['picture url'] = picurl
                dic['website'] = self.url
                dic['snapshot time'] = shot_info
                dic['crawling time'] = crawling_time
                fs.put(data, **dic)
        except Exception as e:
            raise e
        else:
            print(str(self.url) + " :get available imgs and save metadata !")
