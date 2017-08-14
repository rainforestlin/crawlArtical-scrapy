# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
from scrapy.loader import ItemLoader
#MapCompose是将至少一个函数组合在一起.TakeFirst是取list中的第一个。Join即是将list中的数据连接起来
from scrapy.loader.processors import TakeFirst,MapCompose,Join
from .util.common import get_md5


class JobboleArticleItemLoader(ItemLoader):
    default_output_processor=TakeFirst()


def get_num(value):
    num_match = re.match(".*?(\d+).*", value)
    if num_match is not None:
        num = int(num_match.group(1))
    else:
        num = 0
    return num


def convert_date(value):
    try:
        create_time=datetime.datetime.strptime(value,'%Y/%m/%d').date()
    except Exception as e:
        create_time = datetime.datetime.now().date()
    return create_time


def set_md5(value):
    return get_md5(value)
# 将tag中的评论删掉


def clear_conment(value):
    if "评论" in value:
        return ""
    else:
        return value


# 返回需要使用list结构的值
def return_value(value):
    return value


class JobboleArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    create_time=scrapy.Field(
        # 只需要单个处理函数时，可以不实用MapCompose
        input_processor=convert_date
    )
    post_url=scrapy.Field()
    tag_name=scrapy.Field(
        input_processor=MapCompose(clear_conment),
        output_processor=Join(",")
    )
    praise_count=scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    conment=scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    bookmark_count=scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    content=scrapy.Field()
    # 因为在imagepipeline时需要使用到的结构是list，所以要覆盖掉takefirst
    front_image_url=scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    url_object_id=scrapy.Field(
        input_processor=MapCompose(set_md5)
    )
