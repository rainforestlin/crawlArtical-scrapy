import requests
#python2中是cookielib，Python3中是http下的cookiejar
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re
import json
import time
from PIL import Image




agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"
headers = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
    "User-Agent":agent
}
# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")

# 获得_xsrf
def get_xsrf():
    response=session.get("https://www.zhihu.com",headers=headers)
    match_obj= re.match('.*name="_xsrf" value="(.*?)"',response.text,re.S)

    if match_obj:
        return match_obj.group(1)
    else:
        return ""

# 获取验证码
def get_captcha():

    # t = str(int(time.time() * 1000))
    # captcha_url = "https://www.zhihu.com/captcha.gif?r=%s&type=login"%t
    captcha_url = "https://www.zhihu.com/captcha.gif?&type=login"
    captcha_image = session.get(captcha_url, headers=headers)
    with open('captcha.gif', 'wb') as f:
        f.write(captcha_image.content)
        f.close()
    try:
        im=Image.open("captcha.gif")
        im.show()
        captcha = input("please input the captcha:")
        im.close()
        return captcha
    except:
        print("未打开验证码文件")



def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False
def zhihu_login(account, password):
    #知乎登录
    if re.match("^1\d{10}",account):
        print ("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
        }
    else:
        if "@" in account:
            # 判断用户名是否为邮箱
            print("邮箱方式登录")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password,
            }

    response = session.post(post_url, data=post_data, headers=headers)
    login_msg = json.loads(response.text)
    #判断是否需要输入验证码
    if login_msg["r"]==1:
        post_data["captcha"]=get_captcha()
        response = session.post(post_url,data=post_data,headers=headers)
        print(json.loads(response.text)["msg"])
    session.cookies.save()

if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
        account = input('请输入你的用户名\n>  ')
        password = input("请输入你的密码\n>  ")
        zhihu_login(account, password)