# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
from scrapy.loader import ItemLoader
# MapCompose是将至少一个函数组合在一起.TakeFirst是取list中的第一个。Join即是将list中的数据连接起来
from scrapy.loader.processors import TakeFirst,MapCompose,Join
from .util.common import get_md5

# 重写ItemLoader


class JobboleArticleItemLoader(ItemLoader):
    default_output_processor=TakeFirst()


def get_num(value):
    num_match = re.match(".*?(\d+).*", value)
    if num_match is not None:
        num = int(num_match.group(1))
    else:
        num = 0
    return num

# 标准化时间


def convert_date(value):
    try:
        date = value[0].split()[0]
        create_time=datetime.datetime.strptime(date,'%Y/%m/%d').date()
    except Exception as e:
        print("时间错了")
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
    def get_insert_sql(self):
        insert_sql = """
                 insert into jobbole_article(url_object_id,title,create_time,tag_name
                            ,praise_count,conment_count
                            ,bookmark_count,content,front_image_url,post_url
                        )
                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        params = (self["url_object_id"],self["title"],self["create_time"],
                                        self["tag_name"],self["praise_count"],self["conment"],
                                        self["bookmark_count"],self["content"],self["front_image_url"],
                                        self["post_url"]
                                        )
        return insert_sql,params


class ZhihuQuestionItem(scrapy.Item):
    #知乎question的item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    # creat_time = scrapy.Field()
    # update_time = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
                 insert into zhihu_question(zhihu_id,topics,url,title,content,answer_num,comments_num,
                                            watch_user_num,click_num
                        )
                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        params = (self["zhihu_id"],self["topics"],self["url"],
                                        self["title"],self["content"],self["answer_num"],self["comments_num"],
                                        self["watch_user_num"],self["click_num"]
                                        )
        return insert_sql,params

class ZhihuAnswerItem(scrapy.Item):
    #知乎回答的Item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
                 insert into zhihu_answer(zhihu_id,url,question_id,author_id,author_name,
                                          content,creat_time,praise_num,comments_num
                        )
                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        params = (self["zhihu_id"],self["url"],self["question_id"],
                                        self["author_id"],self["author_name"],self["content"],self["create_time"],
                                        self["praise_time"],self["comments_num"]
                                        )
        return insert_sql,params
