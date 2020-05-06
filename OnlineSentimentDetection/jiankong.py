# -*-coding:utf-8 -*-

'''
@File       : jiankong.py
@Author     : W Li, TY Liu
@Date       : 2020/5/1
@Desc       : 项目后台服务
'''
from flask import Flask, render_template, request, jsonify
import time, pymysql
from database import data_util
from predictors.predictor import Predictor
from models.BiLSTM.bilstm import BiLSTM
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("monitor.html")


@app.route('/time')
def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年","月","日")


@app.route('/u1')
def get_u1_data():
    sql = "select 正面,负面,中性 from pie where 来源='微信'"
    data = data_util.query(sql)
    jj = jsonify({"pos":data[0][0],"neg":data[0][1],"neu":data[0][2]})
    return jj

@app.route('/u2')
def get_u2_data():
    sql = "select 正面,负面,中性 from pie where 来源='微博'"
    data = data_util.query(sql)
    jj = jsonify({"pos":data[0][0],"neg":data[0][1],"neu":data[0][2]})
    return jj

@app.route('/u3')
def get_u3_data():
    sql = "select 正面,负面,中性 from pie where 来源='美团'"
    data = data_util.query(sql)
    jj = jsonify({"pos":data[0][0],"neg":data[0][1],"neu":data[0][2]})
    return jj

@app.route('/d1')
def get_d1_data():
    sql = "select 项目,数量 from bar where 平台='资讯'"
    da = list(data_util.query(sql))
    data = sorted(da, key = lambda k: k[1], reverse=True)[:5]
    xm = []
    sl = []
    for i in range(5):
        xm.append(data[i][0])
        sl.append(data[i][1])
    jj = jsonify({"xm":xm,"sl":sl})
    return jj

@app.route('/d2')
def get_d2_data():
    sql = "select 项目,数量 from bar where 平台='口碑'"
    da = list(data_util.query(sql))
    data = sorted(da, key = lambda k: k[1], reverse=True)[:5]
    xm = []
    sl = []
    for i in range(5):
        xm.append(data[i][0])
        sl.append(data[i][1])
    jj = jsonify({"xm":xm,"sl":sl})
    return jj

if __name__ == '__main__':
    # TODO 准备项目启动参数

    # 启动爬虫
    # TODO 测试
    crawler_run_cmd = 'python ./spider/meituan_comments/run.py'
    # os.system(crawler_path)
    os.popen(crawler_path)

    # 准备模型
    # TODO 多模型
    weights_path = "./bilstm_weights"
    lstm = BiLSTM()
    lstm.load_weights(weights_path)
    models = [lstm]

    # 启动预测任务
    pred = Predictor(100, models)
    pred.predict()

    # 启动flask
    app_ctx = app.app_context()
    app_ctx.push()
    #print(get_d1_data())
    app.run(debug=True)
    app_ctx.pop()


