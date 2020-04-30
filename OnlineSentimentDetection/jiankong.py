from flask import Flask, render_template, request, jsonify
import time, pymysql

app = Flask(__name__)

def get_conn():
    # 建立连接
    conn = pymysql.connect(host="localhost", user="root", password="###", db="monitor", charset="utf8")
    # c创建游标A
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql,*args):
    """

    :param sql:
    :param args:
    :return:
    """
    conn,cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res



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
    data = query(sql)
    jj = jsonify({"pos":data[0][0],"neg":data[0][1],"neu":data[0][2]})
    return jj

@app.route('/u2')
def get_u2_data():
    sql = "select 正面,负面,中性 from pie where 来源='微博'"
    data = query(sql)
    jj = jsonify({"pos":data[0][0],"neg":data[0][1],"neu":data[0][2]})
    return jj

@app.route('/u3')
def get_u3_data():
    sql = "select 正面,负面,中性 from pie where 来源='美团'"
    data = query(sql)
    jj = jsonify({"pos":data[0][0],"neg":data[0][1],"neu":data[0][2]})
    return jj

@app.route('/d1')
def get_d1_data():
    sql = "select 项目,数量 from bar where 平台='资讯'"
    da = list(query(sql))
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
    da = list(query(sql))
    data = sorted(da, key = lambda k: k[1], reverse=True)[:5]
    xm = []
    sl = []
    for i in range(5):
        xm.append(data[i][0])
        sl.append(data[i][1])
    jj = jsonify({"xm":xm,"sl":sl})
    return jj

if __name__ == '__main__':
    app_ctx = app.app_context()
    app_ctx.push()
    #print(get_d1_data())
    app.run(debug=True)
    app_ctx.pop()


