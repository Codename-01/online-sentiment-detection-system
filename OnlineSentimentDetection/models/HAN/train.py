# -*-coding:utf-8 -*-

'''
@File       : __init__.py.py
@Author     : HW Shen
@Date       : 2020/4/20
@Desc       :
'''

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.compat.v1.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from models.HAN.han import HierarchicalAttentionNetworks
from models.HAN.DataUtil import read_yelp_dataset, read_dp_db_dataset
import os

max_features = 5000
maxlen_sentence = 16
maxlen_word = 232  # 每句话最多个单词个数，不足的在前面补0
batch_size = 32
embedding_size = 300
epochs = 10

print('Loading data...')

x_train, y_train, x_test, y_test = read_dp_db_dataset()  # 点评+豆瓣数据

print(len(x_train), 'train sequences')
print(len(x_test), 'test sequences')

print('Pad sequences (samples x #sentence x #word)...')
x_train = pad_sequences(x_train, maxlen=maxlen_sentence * maxlen_word)
x_test = pad_sequences(x_test, maxlen=maxlen_sentence * maxlen_word)
x_train = x_train.reshape((len(x_train), maxlen_sentence, maxlen_word))
x_test = x_test.reshape((len(x_test), maxlen_sentence, maxlen_word))
print(x_train[0])
print('x_train shape:', x_train.shape)
print(x_test[0])
print('x_test shape:', x_test.shape)

print('Build model...')
model = HierarchicalAttentionNetworks(maxlen_sentence, maxlen_word, max_features, embedding_size)
model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])

print('Train...')

# early stoping, 如果3个epoch内 validation loss 没有改善则停止训练
early_stopping = EarlyStopping(monitor='val_accuracy', patience=3, mode='max')


# 创建一个保存模型权重的回调
checkpoint_path = "HAN_training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

# training
model.fit(x_train,
          y_train,
          batch_size=batch_size,
          epochs=epochs,
          callbacks=[early_stopping],
          validation_data=(x_test, y_test))

print('Test...')
result = model.predict(x_test)

