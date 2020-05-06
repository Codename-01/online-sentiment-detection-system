# -*-coding:utf-8 -*-

'''
@File       : bilstm.py
@Author     : HW Shen, TY Liu
@Date       : 2020/5/1
@Desc       : 双向lstm模型构建
'''
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Bidirectional

class BiLSTM:
    def __init__(self):
        '''
        初始化模型结构
        '''
        embedding_dim = 300
        num_words = 50000 # 只使用前50000个词
        model = Sequential()
        model.add(Embedding(num_words,embedding_dim,
                            input_length=max_tokens,
                            trainable=False))
        model.add(Bidirectional(LSTM(units=64, return_sequences=True)))
        model.add(LSTM(units=16, return_sequences=False))
        model.add(Dense(1, activation='sigmoid'))
        self.model = model

    def load_weights(self, weights_path):
        '''
        读取模型权重
        --------------
        weights_path: 权重文件路径
        '''
        self.model.load_weights(weights_path)

    def predict(self, data):
        '''
        应用模型，预测结果
        ---------------
        data: 已处理过的待预测数据
        '''
        pred = model.predict(data)
        return pred