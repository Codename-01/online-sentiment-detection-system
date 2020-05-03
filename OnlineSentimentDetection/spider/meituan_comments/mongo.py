# -*-coding:utf-8 -*-

import pymongo
import pandas as pd


# 连接数据库
client = pymongo.MongoClient('192.168.1.16', 37017)
db = client['meituan']
table = db['maoyan_movies']

# 读取数据
pd_data = pd.DataFrame(list(table.find()))
# print(pd_data['user_id'])

# 选择需要显示的字段
movie_ids = pd_data['movie_id'].tolist()

# 打印输出
print(len(movie_ids))

print(len(set(movie_ids)))

with open("movie_id.csv", 'w', encoding='utf-8') as fw:
    for id in movie_ids:
        fw.write(str(id) + "\n")