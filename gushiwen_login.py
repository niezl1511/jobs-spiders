import requests
from bs4 import BeautifulSoup

s = requests.Session()

# 分析 ： 账户密码   验证码  密文（post指令_csrf）
# 验证码和密文都需要从登录页面中获取
login_url = "https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
# 访问登录页面，获取验证码和密文
r = s.get(url=login_url,headers=headers)
# 通过bs4来解析网页
soup = BeautifulSoup(r.text,'lxml')
a = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')
b = soup.select('#__VIEWSTATE')[0].attrs.get('value')

# 获取验证码图片的url
img_url = "https://so.gushiwen.org" + soup.select("#imgCode")[0].attrs.get('src')
img = s.get(img_url)
# print(img.content)
with open("./yangzhengma.png",'wb') as fp:
    fp.write(img.content)
# 验证码图片已经被下载，接下来识别验证码：人工识别或者机器识别
code = input("请输入验证码：")

# 创建请求头和请求体发起post请求去登录
post_url = "https://so.gushiwen.org/user/login.aspx?from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx"
data = {
    '__VIEWSTATE':	b,
    '__VIEWSTATEGENERATOR':a,
    'from':'http://so.gushiwen.org/user/collect.aspx',
    'email':'fanjianbo666@163.com',
    'pwd':'123456',
    'code':	code,
    'denglu':'登录'
}
r = s.post(url=post_url,headers=headers,data=data)
print(r.text)
# 作业：把所有的“古诗”、“名句”，“作者”，“古籍”爬取下来放到json文件中




