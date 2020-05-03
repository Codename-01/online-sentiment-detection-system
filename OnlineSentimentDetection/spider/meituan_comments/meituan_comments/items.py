# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanCommentsItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MaoyanCommentsItem(scrapy.Item):

    """ 猫眼电影评论信息 """

    cityName = scrapy.Field()
    nickName = scrapy.Field()
    user_id = scrapy.Field()
    movieId = scrapy.Field()
    gender = scrapy.Field()
    content = scrapy.Field()
    score = scrapy.Field()
    comment_time = scrapy.Field()


class MaoyanMovieItem(scrapy.Item):

    """ 猫眼电影名称+Id """

    name = scrapy.Field()
    movie_id = scrapy.Field()







