# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import codecs
import json
import pymysql
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi #使用twisted将mysql的操作异步化


class CrawlarticalPipeline(object):
    def process_item(self,item,spider):
        return item


class JsonWithEncodingPipeline(object):
    '''
    json的encoder无法将date存入到json文件中，会报出错误
     Object of type 'date' is not JSON serializable
    该clas为自定义的json文件导出
    '''
    def __init__(self):
        self.file = codecs.open('Artical.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()
class JsonExporterPipeline(object):
    #调用scrapy自己提供的JsonExporter
    def __init__(self):
        self.file=open("articalexporter.json","wb")
        self.exporter=JsonItemExporter(self.file,encoding="utf8",ensure_ascii=False)
        self.exporter.start_exporting()
    def spider_closed(self):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
class MysqlPipeline(object):
    # 自己写的mysql写入。考虑到scrapy的爬取速度应该是大于MySQL写入速度。容易形成阻塞，需要进行异步操作
    def __init__(self):
        self.conn=pymysql.connect("localhost","root","","Crawl",charset="utf8",use_unicode=True)
        self.cursor=self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql="""
         insert into jobbole_article(url_object_id,title,create_time,tag_name
                    ,praise_count,conment_count
                    ,bookmark_count,content,front_image_url,post_url
                )
                 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["url_object_id"],item["title"],item["create_time"],
                                        item["tag_name"],item["praise_count"],item["conment"],
                                        item["bookmark_count"],item["content"],item["front_image_url"],
                                        item["post_url"]
                                        ))
        self.conn.commit()
        return item

class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls,settings):
        dbparms=dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,#选择用字典结构返回cursor
            use_unicode=True
        )
        dbpool=adbapi.ConnectionPool("pymysql",**dbparms)
        return cls(dbpool)
    def process_item(self,item,spider):
        #使用twisted将mysql插入进行异步化
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)#处理异常
    def handle_error(self,failure):
        print(failure)

    def do_insert(self,cursor,item):
        # 执行具体的插入.会通过dbpool.runInteraction进行自动的异步提交
        insert_sql="""
         insert into jobbole_article(url_object_id,title,create_time,tag_name
                    ,praise_count,conment_count
                    ,bookmark_count,content,front_image_url,post_url
                )
                 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_sql,(item["url_object_id"],item["title"],item["create_time"],
                                        item["tag_name"],item["praise_count"],item["conment"],
                                        item["bookmark_count"],item["content"],item["front_image_url"],
                                        item["post_url"]
                                        ))

class ArticalImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path=value["path"]
            item["front_image_url"]=image_file_path
        return item

