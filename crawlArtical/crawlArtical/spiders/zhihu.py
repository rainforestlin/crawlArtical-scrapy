import scrapy
import re
from PIL import Image
import json
from urllib import parse
from scrapy.loader import ItemLoader
from ..items import ZhihuAnswerItem,ZhihuQuestionItem
class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains=["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/explore']
    headers={
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    'Connection': 'keep - alive',
    }
    def parse(self, response):
        """
        提取出check_login中yield中的URL即为知乎首页
        将其中所有的URL中类似/question/xxxx的URL提取出来，然后下载后放入解析函数
        :param response: 
        :return: 
        """
        all_urls = response.css("a::attr(href)").extract()

        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x:True if x.startswith("https") else False,all_urls)
        for url in all_urls:
            print(url)
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*",url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(request_url,
                                     headers=self.headers,
                                     meta={"question_id":question_id},
                                     callback=self.parse_question)
    def parse_question(self,response):
        """
        处理question页面，从页面中取出我们需要的item
        :param response: 
        :return: 
        """
        if "QuestionHeader-title" in response.text:
            #知乎的新版本
            item_loader = ItemLoader(item=ZhihuQuestionItem(),response=response)
            item_loader.add_css("title",".QuestionHeader-main .QuestionHeader-title::text")
            item_loader.add_css("topics",".TopicLink .Popover div::text")
            item_loader.add_css("content",".QuestionHeader-detail")
            item_loader.add_value("url",response.url)
            item_loader.add_value("zhihu_id",int(response.meta.get("question_id","")))
            item_loader.add_css("answer_num",".List-headerText span::text")
            item_loader.add_css("watch_user_num",'.NumberBoard-value::text')
            item_loader.add_css("click_num",'.NumberBoard-value::text')
            item_loader.add_css("comments_num",'.QuestionHeader-Comment button::text')

            QuestionItem = item_loader.load_item()
            yield QuestionItem

        else:
            #知乎的老版本
            
            pass
    def start_requests(self):
        #因为要登录后才能查看知乎，所以要重写入口

        return [scrapy.Request("https://www.zhihu.com/#signin",headers=self.headers,meta={"cookiejar":1 },callback=self.login)]

    def login(self,response):

        _xsrf = response.xpath('/html/body/div[1]/div/div[2]/div[2]/form/input/@value').extract_first()
        # account = input("请输入账号\n--->")
        # password = input("请输入密码\n--->")
        account = "13608335855"
        password = "Wxzyydas6"
        if re.match("^1\d{10}", account):
            print("手机号码登录")
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": _xsrf,
                "phone_num": account,
                "password": password,
                "captcha":""
            }
        else:
            if "@" in account:
                # 判断用户名是否为邮箱
                print("邮箱方式登录")
                post_url = "https://www.zhihu.com/login/email"
                post_data = {
                    "_xsrf": _xsrf,
                    "email": account,
                    "password": password,
                    "captcha":""
                }

        captcha_url = "https://www.zhihu.com/captcha.gif?&type=login"
        #因为scrapy是一个异步框架，所以为了保证验证码在同一个session下，就将这个request yield出去
        yield scrapy.Request(url=captcha_url,
                             headers=self.headers,
                             meta={"post_data":post_data,
                                   "post_url":post_url,
                                   "cookiejar":response.meta['cookiejar']},
                             callback=self.login_after_captcha)

    def login_after_captcha(self,response):
        #获取验证码
        post_data = response.meta.get("post_data","")
        post_url = response.meta.get("post_url","")
        with open('captcha.gif', 'wb') as f:
            f.write(response.body)
        try:
            im = Image.open("captcha.gif")
            im.show()
            captcha = input("please input the captcha:")
        except:
            print("未打开验证码文件")
        post_data["captcha"] = captcha
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            meta={"cookiejar":response.meta['cookiejar']},
            callback=self.check_login
        )]
    def check_login(self,response):
        response_text = json.loads(response.body)
        print(response.meta.get("cookiejar"))
        if response_text["r"] == 0:
            #登录成功后才开始使用start_urls
            for url in self.start_urls:
                yield scrapy.Request(url,headers=self.headers,dont_filter=True)
