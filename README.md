# online-sentiment-detection-system 在线舆情监测系统

#### 项目背景
随着互联网特别是移动互联网社交APP高速发展， 不论是政府还是企业，甚至于个人，网络舆情监测都显得越来越重要。
舆情分析系统的核心技术在于舆情分析引擎，涉及的最主要的技术包括文本分类、聚类、观点倾 向性识别、主题检测与跟踪、自动摘要等计算机 文本信息内容识别技术。

本项目希望通过应用尽可能多的方法（机器学习，深度学习等），对不同来源数据进行训练、测试和评估。以便了解不同模型在不同的数据情况下的表现。


#### 文件结构介绍
* config文件：配置各种模型的配置参数
* data：存放原始数据raw data，停用词stopwords
* preprocess：提供数据预处理的方法
* outputs：存放 vocab，word_to_index, label_to_index 处理后的数据
* models：存放模型代码
* trainers：存放训练代码
* predictors：存放预测代码


#### 团队组成
本项目由4人小组协作完成：howling0, Codename-01, omige, xiaobuguilaile

#### 使用情感分析模型(基于ALBERT)
1. 安装transformers包
```
pip install transformers -i https://mirrors.aliyun.com/pypi/simple/
```
2. 确保torch，cuda已经正确安装(如果cuda没有安装的话可能会用cpu进行计算，速度会下降)
3. 将需要进行判断的句子保存为test.json，并放在data文件夹中对应的分类中，例如restaurant，存储格式如下
```
{"index":0,"comment":"非常垃圾，菜里面都是石头，服务员态度极差"}
{"index":1,"comment":"太好吃了，我吃了这么多年日料，这是我吃过的最好吃的一次"}
{"index":2,"comment":"一般一般，在同等档次的餐厅中中规中举吧"}
```
4. 运行predict_restaurant.sh
```
bash predict_restaurant.sh
```

#### 后续改进
1. 预测结果存储于data/restaurant/test_prediction.json中
2. 后续可能会针对四种场景训练四个不同的模型，当前只做了restaurant的模型，保存在models/albert_restaurant中，后续模型需要和它平行放置