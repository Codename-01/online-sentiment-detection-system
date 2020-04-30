# -*- coding: utf-8 -*-

import scrapy
from meituan_comments.items import MaoyanMovieItem
from loguru import logger


class MaoyanMovieIdSpider(scrapy.Spider):

    name = 'maoyan_movie_id'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def __init__(self):
        super(MaoyanMovieIdSpider, self).__init__()

        logger.add("log/maoyan_movieId_{time}.log", encoding='utf-8')

        self.base_url = 'https://maoyan.com/films?showType=3&offset={}'

        self.cookies = {'HMACCOUNT': '2650599DB2C5C3A3',
                        'BAIDUID': '3A607321FF7C706AD887C08F1844B905:FG',
                        'PSTM': '1585483110', 'BIDUPSID': '92C364A791A71B0F04E6DA53D1B30230',
                        'HMACCOUNT_BFESS': '2650599DB2C5C3A3',
                        'BDUSS': 'NFcFhSVDF-MjQxd2VxfnVLNThoa0R5cHo5cTY0SlB3ckkxNTJoZEt3TU9xYlplSVFBQUFBJCQAAAAAAAAAAAEAAAD1qVQVx9i46M6qy63ZqQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4cj14OHI9ebT',
                        'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
                        'BDSFRCVID': 'sCLOJexroG3Hp2bu6Y4St3dw9gKK0gOTDYLEHWJAh7T2grFVNlZIEG0PtoWBG_u-K4eiogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
                        'H_BDCLCKID_SF': 'JbAjoKK5tKvbfP0kh-QJhnQH-UnLqbIfW67Z0lOnMp05OMjSjnoEyq_QqH3Hbp_q5554atJKQfcW8DO_e6KBjjvQeatDq-7KaDPXoI_2fIPWKRrN554hqtPgyxomtjjmBNQA-4QaJJk5q4-RbbtBb-TbKxjNLUkqKm5ebRck0qosJRo5XMc4WjtAQttjQPROfIkja-5tytnKjn7TyU42bf47yhjl0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OhJRLDoI_KJDDKMKvFKCTqht4HbquX5-Cs3R6l2hcH0KLKV4QCbl3G5jKf3N3JJ-3ffCkHKD5HtMb1MRjvMDc6b-k7K4OZWhJ8QbCOWq5TtUJrJKnTDMRhqfKgX-TyKMnitIT9-pnK3qQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDj0Kj65LDG8saJDX5CjyWJ5XHJO_bIJT0MnkbfJBDR5q-t5TL6IqBh_5bIOffITTDxDhbjt7yajK2-FLLKn3-PogWq76Jf0le-TpQT8rBpAOK5Oib4jl2hRkab3vOIJNXpO15xKzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqjFOJbFH_KPQb-3bK4nY-tnshPCsKU7tetJyaR3HhpRvWJ5WqR7jDU7fLx40jxbhQb0e5Tk80hvc5KTxShbXXMoRKl8qybDJKl_fbGcwbjCa3l02V--9Mj3ThnQDbM4OJ-RMW20j0h7mWIQvsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjjCbDTOyjHteqbbfb-oQ3R3Ob6rjDnCrKUbdXUI82h5y05J7-nraLCQwJUOMhnb6etJvyT8sXnORXx74WNvZ5RP5QIoJqlQKX4vAyfL1Db3J2hbG3aOtslk25RToepvoD-Jc3MvByPjdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEK5r2SC8XfCL-3q',
                        'delPer': '0', 'PSINO': '5', 'HMVT': '6bcd52f51e9b3dce32bec4a3997715ac|1588067128|',
                        'BDRCVFR[feWj1Vr5u3D]': 'mk3SLVN4HKm', 'H_PS_PSSID': '31359_1455_31326_21126_31421_31341_30903_31463_31229_30824_31163_22160'}

    def start_requests(self):

        yield scrapy.Request(
            url=self.base_url.format(0),
            cookies=self.cookies,
            meta={"offset":0}
        )

    def parse(self, response):

        print(response.url)

        logger.info(response.url)

        offset = response.meta["offset"]
        movie_li = response.xpath('//div[@class="movie-item film-channel"]/..')

        logger.info("movie_li: " + str(movie_li))

        for mov in movie_li:

            item = MaoyanMovieItem()

            item["name"] = mov.xpath('div[@class="channel-detail movie-item-title"]/@title').extract_first()
            movie_id = mov.xpath('div[@class="channel-detail movie-item-title"]/a/@data-val').extract_first()
            item["movie_id"] = movie_id.replace("{movieId:", "").replace("}", "")

            yield item

        offset += 30

        if len(movie_li) != 0:
            yield scrapy.Request(url=self.base_url.format(offset),
                                 cookies=self.cookies,
                                 callback=self.parse,
                                 meta={"offset": offset}
                                 )

