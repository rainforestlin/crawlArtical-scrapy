import scrapy,re
from ..items import JobboleArticleItem
from scrapy.http import Request
from urllib import parse
from ..util.common import get_md5
import datetime

# from scrapy.loader import ItemLoader#默认的loader
from ..items import JobboleArticleItemLoader


class crawlJobbole(scrapy.Spider):
    name = "jobbole"
    allowed_domains=["jobbole.com"]
    start_urls=["http://blog.jobbole.com/all-posts/"]
    def parse(self, response):
        #提取出列表页文章的链接以及封面链接
        urls= response.css("#archive .post-thumb a")
        for url in urls:
            front_image_url=url.css("img::attr(src)").extract()[0]
            post_url=url.css("::attr(href)").extract()[0]
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":front_image_url},callback=self.parse_detail)
        #提取出下一页
        next_page=response.css(".next.page-numbers::attr(href)").extract_first()
        yield Request(next_page,self.parse)
    def parse_detail(self,response):
        # jobbloe_ArticalItem=JobboleArticalItem()
        #
        # sel=scrapy.Selector(response)
        #
        # title=sel.xpath("//div[@class='entry-header']/h1/text()").extract()[0]
        # create_time=sel.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace(' ·','')
        praise_count=response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()")
        # if len(praise_count) is not 0:
        #     praise_count=praise_count.extract()[0]
        # else:
        #     praise_count=0
        #
        # #取出的收藏数中有"收藏"两个字，去除后只留下收藏数
        # bookmark=sel.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # bookmark_match=re.match(".*?(\d+).*",bookmark)
        # if bookmark_match is not None:
        #     bookmark_count=int(bookmark_match.group(1))
        # else:
        #     bookmark_count=0
        #
        # #评论数
        # conment=sel.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # conment_match=re.match(".*?(\d+).*",conment)
        # if conment_match is not None:
        #     conment_count=int(conment_match.group(1))
        # else:
        #     conment_count=0
        #
        # #选择tag，去除掉其中的评论，然后用"，"连接
        # tag=sel.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_name="，".join([element for element in tag if not element.strip().endswith("评论")])
        # #获取到封面的地址
        # front_image_url=response.meta.get("front_image_url","")
        # content=sel.xpath("//div[@class='entry']").extract()[0]
        #
        #
        # jobbloe_ArticalItem["title"]=title
        # try:
        #     create_time=datetime.datetime.strptime(create_time,'%Y/%m/%d').date()
        # except Exception as e:
        #     create_time = datetime.datetime.now().date()
        # jobbloe_ArticalItem["create_time"]=create_time
        # jobbloe_ArticalItem["praise_count"]=praise_count
        # jobbloe_ArticalItem["bookmark_count"]=bookmark_count
        # jobbloe_ArticalItem["conment"]=conment_count
        # jobbloe_ArticalItem["content"]=content
        # jobbloe_ArticalItem["post_url"]=response.url
        # jobbloe_ArticalItem["tag_name"]=tag_name
        # jobbloe_ArticalItem["front_image_url"]=[front_image_url]
        # jobbloe_ArticalItem["url_object_id"]=get_md5(response.url)
        front_image_url = response.meta.get("front_image_url", "")
        jobbloe_ArticalItem=JobboleArticleItemLoader(item=JobboleArticleItem(),response=response)
        jobbloe_ArticalItem.add_xpath("title","//div[@class='entry-header']/h1/text()")
        jobbloe_ArticalItem.add_xpath("create_time","//p[@class='entry-meta-hide-on-mobile']/text()")
        # prais_count字段用了两个XPath选择器。是为了防止第一个选择器采集的数据为[]无法传入到itemloader的processor中进行处理
        jobbloe_ArticalItem.add_xpath("praise_count","//span[contains(@class,'vote-post-up')]/h10/text()")
        jobbloe_ArticalItem.add_xpath("praise_count","//span[contains(@class,'vote-post-up')]/text()")

        jobbloe_ArticalItem.add_xpath("bookmark_count","//span[contains(@class,'bookmark-btn')]/text()")
        jobbloe_ArticalItem.add_xpath("conment","//a[@href='#article-comment']/span/text()")
        jobbloe_ArticalItem.add_value("post_url",response.url)
        jobbloe_ArticalItem.add_xpath("tag_name","//p[@class='entry-meta-hide-on-mobile']/a/text()")
        jobbloe_ArticalItem.add_xpath("content","//div[@class='entry']")
        jobbloe_ArticalItem.add_value("front_image_url",front_image_url)
        jobbloe_ArticalItem.add_value("url_object_id",response.url)
        jobbloe_ArticalItem = jobbloe_ArticalItem.load_item()
        yield jobbloe_ArticalItem