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