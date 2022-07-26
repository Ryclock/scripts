"""
 入口文件
"""
from apscheduler.schedulers.blocking import BlockingScheduler

from run_spider import run_spider


def job(website, metadatabase) -> None:
    """
    job 运行脚本

    Args:
        website (str): 目标网站
    """
    run_spider(website, metadatabase)


if __name__ == '__main__':
    website = 'https://news.youth.cn/'
    scheduler = BlockingScheduler()
    scheduler.add_job(job, trigger='interval', hours=2, jitter=120,
                      kwargs={"website": website,
                              'metadatabase': 'metadatabase'})
    scheduler.start()
