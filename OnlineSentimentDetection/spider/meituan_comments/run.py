# -*-coding:utf-8 -*-

from scrapy import cmdline


# cmd = 'scrapy crawl maoyan_movie_id'
cmd = 'scrapy crawl maoyan_movie_comments'
cmdline.execute(cmd.split())