# -*-coding:utf-8 -*-

'''
@File       : __init__.py.py
@Author     : HW Shen
@Date       : 2020/4/20
@Desc       :
'''

import json
import pickle
import nltk
from nltk.tokenize import WordPunctTokenizer
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import jieba
from gensim.models import KeyedVectors
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences


def read_yelp_dataset():

    with open('yelp_data', 'rb') as f:
        data_x, data_y = pickle.load(f)
        data_x, data_y = pickle.load(f)
        length = len(data_x)
        train_x, dev_x = data_x[:int(length * 0.9)], data_x[int(length * 0.9)+1:]
        train_y, dev_y = data_y[:int(length * 0.9)], data_y[int(length * 0.9)+1:]

        return train_x, train_y, dev_x, dev_y


def read_dp_db_dataset():
    with open('dp&db_mebedding_data', 'rb') as f:
        data_x, data_y = pickle.load(f)
        length = len(data_x)
        train_x, dev_x = data_x[:int(length * 0.9)], data_x[int(length * 0.9)+1:]
        train_y, dev_y = data_y[:int(length * 0.9)], data_y[int(length * 0.9)+1:]

        return train_x, train_y, dev_x, dev_y


def chinese_data():

    # dianping数据
    pd_ratings = pd.read_csv('../data/dianping/ratings.csv')
    # douban数据
    pd_comments = pd.read_csv('../data/douban/douban_comments.csv')

    # 剔除NaN所在的行
    new_ratings = pd_ratings.dropna(axis=0, how='any')
    new_ratings.sample(10)
    new_ratings["label"] = new_ratings['rating']
    new_ratings["label"][new_ratings["rating"] >= 3.0] = 1.0
    new_ratings["label"][new_ratings["rating"] < 3.0] = 0.0

    new_comments = pd_comments.dropna(axis=0, how='any')
    new_comments.sample(10)
    new_comments["label"] = new_comments['Star']
    new_comments["label"][new_comments["Star"] >= 3.0] = 1.0
    new_comments["label"][new_comments["Star"] < 3.0] = 0.0

    new_comments["label"] = new_comments["label"].astype('float64')

    # 加载词向量模型
    w2v_model = KeyedVectors.load_word2vec_format('../word2vec/sgns.baidu.word-ngram', binary=False,
                                                  unicode_errors="ignore")

    # 准备训练和测试集
    dianping_comments = new_ratings['comment'].tolist()
    douban_comments = new_comments["Comment"].tolist()
    train_texts_orig = dianping_comments + douban_comments

    dianping_target = new_ratings['label'].tolist()
    douban_target = new_comments['label'].tolist()
    train_target = dianping_target + douban_target

    # 分词
    train_tokens_list = []
    for text in train_texts_orig:

        text = re.sub(r'[^\u4e00-\u9fa5]+', '', text)
        jieba_words = jieba.lcut(text)
        for i, word in enumerate(jieba_words):
            try:
                # 将词转换为索引index
                jieba_words[i] = w2v_model.vocab[word].index
            except KeyError:
                # 如果词不在字典中，则输出0
                jieba_words[i] = 0
        train_tokens_list.append(jieba_words)

    pickle.dump((train_tokens_list, train_target), open('dp&db_mebedding_data', 'wb'))

    # 设置句子最大长度
    num_tokens = [len(tokens) for tokens in train_tokens_list]
    num_tokens = np.array(num_tokens)
    max_tokens = np.mean(num_tokens) + 2 * np.std(num_tokens)
    max_tokens = int(max_tokens)

    # 反向tokenize,# 用来将tokens转换为文本
    # 我们定义一个function，用来把索引转换成可阅读的文本，这对于debug很重要
    def reverse_tokens(tokens):
        text = ''
        for i in tokens:
            if i != 0:
                text = text + w2v_model.index2word[i]
            else:
                text = text + ' '
        return text
    reverse = reverse_tokens(train_tokens_list[0])

    embedding_dim = 300  # 每个词向量的维度
    num_words = 50000  # 只使用前50000个词
    # embedding_matrix为一个 [num_words，embedding_dim] 的矩阵，维度为 50000 * 300
    embedding_matrix = np.zeros((num_words, embedding_dim))  # 初始化 embedding_matrix，之后在keras上进行应用
    for i in range(num_words):
        embedding_matrix[i, :] = w2v_model[w2v_model.index2word[i]]
    embedding_matrix = embedding_matrix.astype('float32')

    # padding（填充）和truncating（修剪)
    maxlen_sentence = 16
    maxlen_word = 232  # 每句话最多个单词个数，不足的在前面补0
    train_pad = pad_sequences(train_tokens_list, maxlen=max_tokens, padding='pre', truncating='pre')
    # train_pad = pad_sequences(train_tokens_list, maxlen=maxlen_sentence * maxlen_word, padding='pre', truncating='pre')

    # 超出五万个词向量的词用0代替
    train_pad[train_pad>=num_words] = 0
    train_target = np.array(train_target)

    # pickle.dump((train_pad, train_target), open('rating_data', 'wb'))
    pickle.dump((train_pad, train_target), open('dp_and_db_mebedding_data', 'wb'))

    X_train, X_test, y_train, y_test = train_test_split(train_pad,
                                                        train_target,
                                                        test_size=0.1,
                                                        random_state=12)

    return X_train, X_test, y_train, y_test


def english_data():
    # 英文分词器
    word_tokenizer = WordPunctTokenizer()
    # 英文分句器
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    # 记录每个单词及其出现的频率
    word_freq = defaultdict(int)

    # 读取数据集（kaggle 数据集），分词，统计频率，保存
    with open('../BaseUtil/data/yelp_academic_dataset_review.json', 'rb') as f:
        for line in f:
            review = json.loads(line)
            words = word_tokenizer.tokenize(review['text'])
            for word in words:
                word_freq[word] += 1
        print('-----------------load finished----------------')

    # 保存词频表
    with open('word_freq.pickle', 'wb') as g:
        pickle.dump(word_freq, g)
        print(len(word_freq))
        print('-------------word_freq save finished----------')

    # 将词表排序，过滤次数最少的三个
    sort_words = list(sorted(word_freq.items(), key=lambda x: -x[1]))
    print("Freq_Top_10_Words: ", sort_words[:10])
    print("Freq_Bottom_10_Words: ", sort_words[-10:])

    # 构建词序表vocab{word:index}，并将出现次数小于5的单词全部去除，视为UNKNOW
    vocab = {}
    i = 1
    vocab['UNKNOW_TOKEN'] = 0
    for word, freq in word_freq.items():
        if freq > 5:
            vocab[word] = i
            i += 1
    print(i)
    UNKNOWN = 0

    # 将所有的评论文件都转化为 30*30 的索引矩阵，也就是每篇都有30个句子，每个句子有30个单词, 不够的补零，多余的删除
    data_x = []
    data_y = []
    max_sent_in_doc = 30
    max_word_in_sent = 30
    num_classes = 5
    with open('../BaseUtil/data/yelp_academic_dataset_review.json', 'rb') as f:
        for line in f:
            doc = []
            review = json.loads(line)
            sents = sent_tokenizer.tokenize(review['text'])  # 获得每篇文章的所有分句
            for i, sent in enumerate(sents):
                if i < max_sent_in_doc:
                    word_to_index = []
                    for j, word in enumerate(word_tokenizer.tokenize(sent)):  # 获得每个分句的所有分词
                        if j < max_word_in_sent:
                            word_to_index.append(vocab.get(word, UNKNOWN))
                    doc.append(word_to_index)
            label = int(review['stars'])
            labels = [0] * num_classes
            labels[label - 1] = 1
            data_y.append(labels)
            data_x.append(doc)
        pickle.dump((data_x, data_y), open('yelp_data', 'wb'))
        print(len(data_x))


if __name__ == '__main__':
    chinese_data()

