import scrapy
import re
from PIL import Image
import json
from urllib import parse
from scrapy.loader import ItemLoader
from ..items import ZhihuAnswerItem,ZhihuQuestionItem
import datetime
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
    #answer第一页的请求URL
    #url为知乎提供的API
    start_answer_urls = "http://www.zhihu.com/api/v4/questions/{0}/answers?" \
                        "sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2" \
                        "Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2" \
                        "Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2" \
                        "Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2" \
                        "Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2" \
                        "Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%" \
                        "5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
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
            #如果提取到question的URL则进行下载
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(request_url,
                                     headers=self.headers,
                                     meta={"question_id":question_id},
                                     callback=self.parse_question)
            # 如果提取到的不是question的URL，则进行跟踪
            else:
                pass
                 # yield scrapy.Request(url,headers=self.headers,callback=self.parse)

    def parse_question(self,response):
        """
        处理question页面，从页面中取出我们需要的item
        :param response:
        :return:
        """
        question_id = response.meta.get("question_id")
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
            yield scrapy.Request(self.start_answer_urls.format(question_id,20,0),headers=self.headers,callback=self.parse_answer)
            yield QuestionItem
            #在question页面中找question的URL
            all_urls = response.css("a::attr(href)").extract()
            all_urls = [parse.urljoin(response.url, url) for url in all_urls]
            all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
            for url in all_urls:
                print(url)
                match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
                # 如果提取到question的URL则进行下载
                if match_obj:
                    request_url = match_obj.group(1)
                    question_id = match_obj.group(2)
                    yield scrapy.Request(request_url,
                                         headers=self.headers,
                                         meta={"question_id": question_id},
                                         callback=self.parse_question)
                # 如果提取到的不是question的URL，则进行跟踪
                else:
                    # pass
                    #若没有发现question的URL，则对获取的URL进行进一步解析
                    yield scrapy.Request(url, headers=self.headers, callback=self.parse)

        else:
            #知乎的老版本

            pass

    def parse_answer(self,response):
        answer_json = json.loads(response.text)
        is_end = answer_json["paging"]["is_end"]
        total_anwsers = answer_json["paging"]["totals"]
        next_url = answer_json["paging"]["next"]
        AnswerItem = ZhihuAnswerItem()
        #提取answer的结构
        for answer in answer_json.get("data"):
            AnswerItem["zhihu_id"] = answer["id"]
            AnswerItem["url"] = answer["url"]
            AnswerItem["question_id"] = answer["question"]["id"]
            AnswerItem["author_id"] = answer["author"]["id"] if "id" in answer["author"] and answer["author"]["id"] is not "0" else None
            AnswerItem["author_name"] = answer["author"]["name"] if "id" in answer["author"] and answer["author"]["id"] is not "0" else "匿名用户"
            AnswerItem["content"] = answer["content"] if "content" in answer else None
            AnswerItem["praise_num"] = answer["voteup_count"]
            AnswerItem["comments_num"] = answer["comment_count"]
            AnswerItem["update_time"] = answer["updated_time"]
            AnswerItem["create_time"] = answer["created_time"]
            AnswerItem["crawl_time"] = datetime.datetime.now()
            yield AnswerItem
        if not is_end:
            yield scrapy.Request(next_url,headers=self.headers,callback=self.parse_answer)


    def start_requests(self):
        #因为要登录后才能查看知乎，所以要重写入口

        return [scrapy.Request("https://www.zhihu.com/#signin",headers=self.headers,callback=self.login)]

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

        return [scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=self.headers,
                meta={"post_data": post_data,
                      "post_url": post_url,
                      },
                callback=self.check_login
            )]
    def login_after_captcha(self,response):
        #获取验证码
        print(response.headers)
        post_data = response.meta.get("post_data","")
        post_url = response.meta.get("post_url","")
        with open('captcha.gif', 'wb') as f:
            f.write(response.body)
        try:
            im = Image.open("captcha.gif")
            im.show()
            captcha = input("please input the captcha:")
            post_data["captcha"] = captcha
        except:
            print("未打开验证码文件")
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login,
        )]
    def check_login(self,response):
        response_text = json.loads(response.body)
        if response_text["r"] == 0:
            headers = response.headers
            cookie = dict(headers)[b'Set-Cookie']
            cookie = [str(c, encoding="utf-8") for c in cookie]
            cookies = ";".join(cookie)
            #登录成功后才开始使用start_urls
            for url in self.start_urls:
                yield scrapy.Request(url,headers=self.headers,dont_filter=True)
        else:
            captcha_url = "https://www.zhihu.com/captcha.gif?&type=login"
            #因为scrapy是一个异步框架，所以为了保证验证码在同一个session下，就将这个request yield出去
            yield scrapy.Request(url=captcha_url,
                                     headers=self.headers,
                                     meta={"post_data":response.meta.get("post_data"),
                                           "post_url":response.meta.get("post_url"),
                                           },
                                     callback=self.login_after_captcha)