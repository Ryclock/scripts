import os

import gridfs
from pymongo import MongoClient

# database = 'src'
database = 'snapshot'
client = MongoClient('127.0.0.1', 27017)  # 连接mongodb
db = client[database]  # 连接对应数据库
fs = gridfs.GridFS(db, collection="news_youth_cn_")  # 连接collection
# 导入
# for filename in os.listdir("C:/Users/15888/Desktop/snapshot/"):
#     dic = {}
#     dic["filename"] = filename
#     content = open("C:/Users/15888/Desktop/snapshot/" + filename, "rb").read()
#     fs.put(content, **dic)
# 导出
for cursor in fs.find():
    filename = cursor.md5
    with open("C:/Users/15888/Desktop/"+database+"/" + filename+".png", "wb") as f:
        f.write(cursor.read())

# !有待改善的网址
# http://www.jwview.com
# https://www.12377.cn
# https://si.trustutn.org/info?sn=820191010038718586352
# http://www.cyyun.com/xxfy/?from=groupmessage&amp;isappinstalled=0
# http://www.people.com.cn
# http://www.newjobs.com.cn
# http://www.newjobs.com.cn
# https://zqb.cyol.com
