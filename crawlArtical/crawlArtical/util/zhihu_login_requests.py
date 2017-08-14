import requests
#python2中是cookielib，Python3中是http下的cookiejar
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re
session = requests.session()
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
headers = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
    "User-Agent":agent
}
def zhihu_login(account,password):
    #知乎登录
    if re.match("^1\d{10}",account):
        print("手机号码登录")
        post_url="https://www.zhihu.com/login/phone_num"
        post_data={
            "_xsrf": get_xsrf(),
            "account": account,
            "password": password

        }
        response = session.post(post_url,data=post_data,headers=headers)
        print(response.text)
        session.cookies.save()
def get_xsrf():
    response=session.get("https://www.zhihu.com",headers=headers)
    match_obj= re.match('.*name="_xsrf" value="(.*?)"',response.text,re.S)

    if match_obj:
        return match_obj.group(1)
    else:
        return ""
zhihu_login("13608335855","Wxzyydas6")