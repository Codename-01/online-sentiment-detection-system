# -*-coding:utf-8 -*-

'''
@File       : data_util.py
@Author     : W Li, TY Liu
@Date       : 2020/5/1
@Desc       : mysql数据库访问
'''
import pymysql

def get_conn(user="root", password="123456", db="monitor"):
    '''
    获取数据库连接
    ---------------
    user: 用户名
    password: 密码
    db: 数据库名
    '''
    # 建立连接
    conn = pymysql.connect(host="localhost", user=user, password=password, db=db, charset="utf8")
    # 创建游标A
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    '''
    关闭数据库连接
    --------------
    conn: 连接信息
    cursor: 游标
    '''
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql,*args):
    """
    数据库查询
    ---------------
    :param sql: sql语句
    :param args: 参数
    :return:
    """
    conn,cursor = get_conn()
    cursor.execute(sql,args)
    conn.commit()
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res

