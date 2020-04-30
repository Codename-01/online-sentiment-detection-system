# -*- coding: utf-8 -*-

import datetime
import json
from loguru import logger
import scrapy
from meituan_comments.items import MaoyanCommentsItem


class MaoyanMovieCommentsSpider(scrapy.Spider):

    name = 'maoyan_movie_comments'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def __init__(self):
        super(MaoyanMovieCommentsSpider, self).__init__()

        # # 创建 rabbitmq 链接，用于提取 movie_id
        # credentials = pika.PlainCredentials("admin", "admin")  # 测试rabbitmq 账号密码
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host="47.98.46.188", port=5672, credentials=credentials))  # 测试环境
        # self.channel = connection.channel()
        # self.channel.queue_declare(queue='maoyan.id', durable=True)  # 创建持久化队列
        # # 预设值: 限制每次由 RabbitMQ 中提取出来的条数(Unacked)为6条，与线程数量TMAX保持一致
        # self.channel.basic_qos(prefetch_count=1)  # 暂改为1条
        # # 通过对接 receiveSpiderNews() 函数，来获取需要处理的新闻
        # self.channel.basic_consume(consumer_callback=self.get_mq_id, queue='maoyan.id', no_ack=True)
        # self.channel.start_consuming()

        self.f = open("meituan_comments/spiders/movie_id.csv", encoding='utf-8')

        logger.add("log/maoyan_comment_{time}.log", encoding='utf-8')  # 日志

        self.base_url = 'http://m.maoyan.com/mmdb/comments/movie/{movie_id}.json?_v_=yes&offset=0&startTime={start_time}'

        self.cookies = {'HMACCOUNT': '2650599DB2C5C3A3',
                        'BAIDUID': '3A607321FF7C706AD887C08F1844B905:FG',
                        'PSTM': '1585483110', 'BIDUPSID': '92C364A791A71B0F04E6DA53D1B30230',
                        'HMACCOUNT_BFESS': '2650599DB2C5C3A3',
                        'BDUSS': 'NFcFhSVDF-MjQxd2VxfnVLNThoa0R5cHo5cTY0SlB3ckkxNTJoZEt3TU9xYlplSVFBQUFBJCQAAAAAAAAAAAEAAAD1qVQVx9i46M6qy63ZqQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4cj14OHI9ebT',
                        'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
                        'BDSFRCVID': 'sCLOJexroG3Hp2bu6Y4St3dw9gKK0gOTDYLEHWJAh7T2grFVNlZIEG0PtoWBG_u-K4eiogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
                        'H_BDCLCKID_SF': 'JbAjoKK5tKvbfP0kh-QJhnQH-UnLqbIfW67Z0lOnMp05OMjSjnoEyq_QqH3Hbp_q5554atJKQfcW8DO_e6KBjjvQeatDq-7KaDPXoI_2fIPWKRrN554hqtPgyxomtjjmBNQA-4QaJJk5q4-RbbtBb-TbKxjNLUkqKm5ebRck0qosJRo5XMc4WjtAQttjQPROfIkja-5tytnKjn7TyU42bf47yhjl0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OhJRLDoI_KJDDKMKvFKCTqht4HbquX5-Cs3R6l2hcH0KLKV4QCbl3G5jKf3N3JJ-3ffCkHKD5HtMb1MRjvMDc6b-k7K4OZWhJ8QbCOWq5TtUJrJKnTDMRhqfKgX-TyKMnitIT9-pnK3qQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDj0Kj65LDG8saJDX5CjyWJ5XHJO_bIJT0MnkbfJBDR5q-t5TL6IqBh_5bIOffITTDxDhbjt7yajK2-FLLKn3-PogWq76Jf0le-TpQT8rBpAOK5Oib4jl2hRkab3vOIJNXpO15xKzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqjFOJbFH_KPQb-3bK4nY-tnshPCsKU7tetJyaR3HhpRvWJ5WqR7jDU7fLx40jxbhQb0e5Tk80hvc5KTxShbXXMoRKl8qybDJKl_fbGcwbjCa3l02V--9Mj3ThnQDbM4OJ-RMW20j0h7mWIQvsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjjCbDTOyjHteqbbfb-oQ3R3Ob6rjDnCrKUbdXUI82h5y05J7-nraLCQwJUOMhnb6etJvyT8sXnORXx74WNvZ5RP5QIoJqlQKX4vAyfL1Db3J2hbG3aOtslk25RToepvoD-Jc3MvByPjdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEK5r2SC8XfCL-3q',
                        'delPer': '0', 'PSINO': '5', 'HMVT': '6bcd52f51e9b3dce32bec4a3997715ac|1588067128|',
                        'BDRCVFR[feWj1Vr5u3D]': 'mk3SLVN4HKm',
                        'H_PS_PSSID': '31359_1455_31326_21126_31421_31341_30903_31463_31229_30824_31163_22160'}

        # 获取当前时间转换为2020/04/29 17:31:15形式空格用%20替换
        self.now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(' ', '%20')

        self.first_moivie_id = 343034

        self.count = 0

    def start_requests(self):

        count = 0
        movie_user_id = int(self.f.readline().strip())
        logger.info("-----------当前处理到的movie_id为----------------: " + str(movie_user_id))
        yield scrapy.Request(
            url=self.base_url.format(movie_id=movie_user_id, start_time=self.now_time),
            cookies=self.cookies,
            callback=self.parse,
            meta={"movie_id":movie_user_id,
                  "count": 0}
        )

    def parse(self, response):

        """ 获取每篇文章的评论 """

        content = json.loads(response.text)

        current_movie_id = response.meta["movie_id"]  # 当前用户的user_id
        current_count = response.meta["count"]
        total_count = content["total"]

        for comment in content["cmts"]:

            # 创建评论item
            # {'cityName': '辽源', 'nickName': '学前班打手', 'user_id': 1099013671, 'movieId': 1211270, 'gender': '暂无','content': '很有意思，喜欢'}
            item = MaoyanCommentsItem()

            item["cityName"] = comment.get("cityName")
            item["nickName"] = comment.get("nickName")
            item["user_id"] = comment.get("user_id")
            item["movieId"] = comment.get("movieId")
            item["gender"] = comment.get("gender")
            if not item["gender"]:
                item["gender"] = "暂无"
            item["content"] = comment.get("content")
            item["score"] = comment.get("score")
            item["comment_time"] = comment.get("startTime")
            # print("item: ", item)
            yield item

        # 是否到最后一页
        # if content.get('cmts', None) is not None:
        if current_count < total_count:

            current_count += 30
            next_time = content["cmts"][-1]["startTime"]

            logger.info('current_movie_id: {}, current count: {}/{}， comment time: {}'.format(current_movie_id, current_count, total_count, next_time))

            # 没到最后一页，就继续跟进
            yield scrapy.Request(
                url=self.base_url.format(movie_id=current_movie_id, start_time=next_time),
                cookies=self.cookies,
                callback=self.parse,
                meta={"movie_id": current_movie_id,
                      "count": current_count}
            )

        else:

            logger.info('content is empty, current movieaId is {}'.format(current_movie_id))

            # 评论到最后一页之后，读入新的 movie_id
            new_movie_id = int(self.f.readline().strip())
            logger.info("-----------当前处理到的 movie_id 为----------------: " + str(new_movie_id))

            yield scrapy.Request(
                url=self.base_url.format(movie_id=new_movie_id, start_time=self.now_time),
                cookies=self.cookies,
                callback=self.parse,
                meta={"movie_id": new_movie_id,
                      "count":0}
            )

