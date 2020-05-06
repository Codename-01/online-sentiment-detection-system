# -*-coding:utf-8 -*-

'''
@File       : predictor.py
@Author     : TY Liu
@Date       : 2020/5/1
@Desc       : 应用模型获取预测结果并存入mysql数据库
'''
from threading import Timer
from database import data_util
from gensim.models import KeyedVectors
import pandas as pd
import pymongo

import logging

class Predictor:
    def __init__(self, predict_interval=30, models=None):
        '''
        初始化预测器配置
        -----------------
        predict_interval: 启动间隔
        models: 模型列表
        '''
        # TODO mongodb 配置，需要读取统一配置
        self.MONGODB_SERVER = '192.168.1.16'
        self.MONGODB_PORT = 37017
        self.MONGODB_DB = 'meituan'
        self.MONGODB_COMMENT_COLLECTION = 'maoyan_comments'
        # 设置mongodb数据集合
        self.client = pymongo.MongoClient(host=self.MONGODB_SERVER, port=self.MONGODB_PORT)
        self.db = self.client[self.MONGODB_DB]
        self.comments_collection = self.db[self.MONGODB_COMMENT_COLLECTION]
        # 定时器启动间隔
        self.predict_interval = predict_interval
        # 模型
        self.models = models
        if not self.models:
            self.models = []
        # 词向量
        self.w2v_model = KeyedVectors.load_word2vec_format('../../../Word2Vec/sgns.baidu.word-ngram', binary=False, unicode_errors="ignore")

    def process_sentence(self, text):
        '''
        处理句子，生成模型(BiLSTM)适用的数据
        -----------------------------------
        text: 原文本内容
        '''
        text = re.sub(r'[^\u4e00-\u9fa5]+', '', text)
        jieba_words = jieba.lcut(text)
        for i, word in enumerate(jieba_words):
            try:
                # 将词转换为索引index
                jieba_words[i] = self.w2v_model.vocab[word].index
            except KeyError:
                # 如果词不在字典中，则输出0
                jieba_words[i] = 0
        return jieba_words

    def predict(self):
        '''
        启动预测任务
        '''
        logging.info("Loading data from mongodb...")
        # 获取数据
        data = [row for row in self.comments_collection.find()]
        # 清空存储
        self.comments_collection.delete_many({})
        logging.info("Predicting using models...")
        # 处理数据
        df = pd.DataFrame(data)['content']
        for i, row in enumerate(df):
            data[i] = process_sentence(row)
        # TODO 输入模型的数据格式可能需要调整
        # 调用模型，获取结果
        # TODO 多模型混合
        data = self.models[0].predict(data)
        logging.info("Saving results to mysql...")
        # 存储结果
        self.save_to_mysql(data)
        #启动定时器任务
        Timer(self.predict_interval, self.predict).start()

    def save_to_mysql(self, data):
        '''
        数据结果处理和mysql存储
        ----------------------
        data: 预测结果列表
        '''
        # TODO 多平台爬取结果处理
        if not data:
            return
        # 取出bar内容
        sql_bar = "select `数量` from `bar` where `平台`='口碑' and `项目`='美团'"
        total = data_util.query(sql_bar)
        # 更新计数
        if total:
            total = int(total[0][0]) + len(data)
            sql_bar = "update `bar` set `数量`=%d where `平台`='口碑' and `项目`='美团'" % total
        else:
            total = len(data)
            sql_bar = "insert into `bar` values('口碑', '美团', %d)" % total
        data_util.query(sql_bar)
        # 取出pie内容
        sql_pie = "select `正面`, `负面`, `中性` from `pie` where `来源`='美团'"
        # 计数
        content = data_util.query(sql_pie)
        p = 0
        m = 0
        n = 0
        if content:
            p += int(content[0][0])
            m += int(content[0][1])
            n += int(content[0][2])
        for d in data:
            if d[0] > 0.5:
                p += 1
            elif d[0] == 0.5:
                m += 1
            else:
                n += 1
        # 更新计数
        sql_pie = "update `pie` set `正面`=%d, `负面`=%d, `中性`=%d where `来源`='美团'" % (p, n, m)
        data_util.query(sql_pie)