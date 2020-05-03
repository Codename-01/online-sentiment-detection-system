# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import json
import pika
import pymongo
import redis
from scrapy.conf import settings
from meituan_comments.items import MaoyanMovieItem, MaoyanCommentsItem


def get_md5(strp):

    """ 哈希算法，对存入的键值value进行加密处理 """

    md5 = hashlib.md5()
    md5.update(str(strp).encode(encoding='utf-8'))
    return md5.hexdigest()


class MeituanCommentsPipeline(object):

    """ 猫眼电影用户评论"""

    def process_item(self, item, spider):
        return item


class MaoyanIdPipeline(object):

    """ 猫眼电影名称+id: 去重+ 存入mongodb """

    def __init__(self):

        # Mongdb
        client = pymongo.MongoClient(host=settings["MONGODB_SERVER"], port=settings["MONGODB_PORT"])
        db = client[settings["MONGODB_DB"]]
        self.movies_collection = db[settings["MONGODB_MOVIE_COLLECTION"]]
        self.comments_collection = db[settings["MONGODB_COMMENT_COLLECTION"]]

        # Redis去重
        pool = redis.ConnectionPool(host=settings["REDIS_HOST"], port=settings["REDIS_PORT"], db=settings["REDIS_DB"])
        self.redis = redis.Redis(connection_pool=pool)

        # Rabbitmq
        credentials = pika.PlainCredentials(settings["MQ_ACCOUNT"], settings["MQ_PASSWORD"])  # 测试rabbitmq 账号密码
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings["MQ_HOST"], port=settings["MQ_PORT"], credentials=credentials, heartbeat=0))  # 测试环境
        self.channel = connection.channel()

    def process_item(self, item, spider):

        if isinstance(item, MaoyanMovieItem):
            key = "MaoyanMoviesId:" + get_md5(item['movie_id'])
            if self.redis.get(key) is None:
                self.redis.set(key, item['name'])
                self.movies_collection.insert(dict(item))  # mongodb存入 movies_collection
                self.channel.basic_publish(exchange=settings["MQ_EXCHANGE"], routing_key='', body=json.dumps(dict(item)))  # rabbitmq存入
                return item

        elif isinstance(item, MaoyanCommentsItem):

            key = "MaoyanComment:" + get_md5(str(item['user_id']) + str(item['movieId']))
            if self.redis.get(key) is None:
                self.redis.set(key, item['content'])
                self.comments_collection.insert(dict(item))  # mongodb存入 comments_collection

                return item


class MaoyanCommentPipeline(object):

    """ 猫眼电影评论comments: 去重+ 存入mongodb """

    def __init__(self):
        # Mongdb
        client = pymongo.MongoClient(host=settings["MONGODB_SERVER"], port=settings["MONGODB_PORT"])
        db = client[settings["MONGODB_DB"]]
        self.comments_collection = db[settings["MONGODB_COMMENT_COLLECTION"]]

        # Redis去重
        pool = redis.ConnectionPool(host=settings["REDIS_HOST"], port=settings["REDIS_PORT"], db=settings["REDIS_DB"])
        self.redis = redis.Redis(connection_pool=pool)

    def process_item(self, item, spider):

        # key = "MaoyanComment:" + get_md5(str(item['user_id']) + str(item['movieId']))
        # if self.redis.get(key) is None:
        #     self.redis.set(key, item['content'])

        self.comments_collection.insert(dict(item))  # mongodb存入 comments_collection

        return item