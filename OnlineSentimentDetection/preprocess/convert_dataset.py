import pandas as pd
import json
from collections import defaultdict

dataset = pd.read_csv("ratings.csv")
clean_set = dataset.dropna()
clean_set = clean_set.sample(200000)
clean_set = clean_set[['comment','rating']]
clean_set['rating'] = clean_set['rating'].astype(int).astype(str)
del dataset
train_dev = clean_set.sample((int(len(clean_set)*0.9)))
test = clean_set[~clean_set.index.isin(train_dev.index)]
test = test.reset_index()
test = test['comment']
test = test.reset_index()
del clean_set
train = train_dev.sample(int(len(train_dev)*0.9))
dev = train_dev[~train_dev.index.isin(train.index)]
del train_dev
f = open("test.json",'w')
test.to_json(f,orient='records',force_ascii=False,lines=True)
f.close()
f = open("train.json",'w')
train.to_json(f,orient='records',force_ascii=False,lines=True)
f.close()
f = open("dev.json",'w')
dev.to_json(f,orient='records',force_ascii=False,lines=True)
f.close()