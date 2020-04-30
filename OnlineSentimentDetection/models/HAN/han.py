# -*-coding:utf-8 -*-

'''
@File       : __init__.py.py
@Author     : HW Shen
@Date       : 2020/4/20
@Desc       :
'''

from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Embedding, Dense, Bidirectional, TimeDistributed, LSTM
from tensorflow.compat.v1.keras.layers import CuDNNLSTM  # only GPU
from models.HAN.attention import Attention


class HierarchicalAttentionNetworks(Model):
    """
    Hierarchical Attention Networks for Document Classification
    HAN 使用了 双向LSTM/GRU 的结构，并且对 Attention 进行调整：
        考虑了Word 层面的 'encoder + attention' 和 Sentence 层面的 'encoder + attention'，
    分别对单词在句子中和句子在文档中的重要性进行了建模。
        word encoder( BiLSTM/BiGRU layer)
        word attention (Attention layer)
        sentence encoder ( BiLSTM / BiGRU layer)
        sentence attention (Attention layer)
    """

    def __init__(self,
                 maxlen_sentence,  # 每句话的最大拆分句子数量
                 maxlen_word,  # 每个句子最大单词数量
                 max_features,
                 embedding_size,
                 class_num=1,  # 默认为2分类
                 last_activation='sigmoid'  # 默认是sigmoid
                 ):
        
        super(HAN, self).__init__()

        self.maxlen_sentence = maxlen_sentence
        self.maxlen_word = maxlen_word
        self.max_features = max_features
        self.embedding_size = embedding_size
        self.class_num = class_num
        self.last_activation = last_activation

        # Word layer
        input_word = Input(shape=(self.maxlen_word,))
        x_word = Embedding(self.max_features, self.embedding_size, input_length=self.maxlen_word)(input_word)
        # x_word = Bidirectional(CuDNNLSTM(128, return_sequences=True))(x_word)  # (only GPU) 双向LSTM or GRU
        x_word = Bidirectional(LSTM(128, return_sequences=True))(x_word)  # 双向LSTM or GRU
        x_word = Attention(self.maxlen_word)(x_word)
        model_word = Model(input_word, x_word)
        self.word_encoder_att = TimeDistributed(model_word)

        # Sentence layer
        # self.sentence_encoder = Bidirectional(CuDNNLSTM(128, return_sequences=True))  # (only GPU) 双向LSTM or GRU
        self.sentence_encoder = Bidirectional(LSTM(128, return_sequences=True))  # 双向LSTM or GRU
        self.sentence_att = Attention(self.maxlen_sentence)

        # Output part
        self.classifier = Dense(self.class_num, activation=self.last_activation)

    def call(self, inputs):

        if len(inputs.get_shape()) != 3:
            raise ValueError('The rank of inputs of HAN must be 3, but now is %d' % len(inputs.get_shape()))
        if inputs.get_shape()[1] != self.maxlen_sentence:
            raise ValueError('The maxlen_sentence of inputs of HAN must be %d, but now is %d' % (self.maxlen_sentence, inputs.get_shape()[1]))
        if inputs.get_shape()[2] != self.maxlen_word:
            raise ValueError('The maxlen_word of inputs of HAN must be %d, but now is %d' % (self.maxlen_word, inputs.get_shape()[2]))

        x_sentence = self.word_encoder_att(inputs)
        x_sentence = self.sentence_encoder(x_sentence)
        x_sentence = self.sentence_att(x_sentence)
        output = self.classifier(x_sentence)

        return output

