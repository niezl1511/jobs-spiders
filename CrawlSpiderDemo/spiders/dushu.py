# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from CrawlSpiderDemo.items import CrawlspiderdemoItem


# crawlspider是spider的一个派生类，crawlspider类定义了一些规则用来提供跟进link的方便机制，可以很方便的从网页中获取link并继续爬取



class DushuSpider(CrawlSpider):
    name = 'dushu'
    allowed_domains = ['dushu.com']
    start_urls = ['http://www.dushu.com/book/1163.html']

    # 这个就是页面的url的匹配规则，我们通过他可以很方便的把我们要爬取的页面匹配出来
    rules = (
        Rule(LinkExtractor(allow=r'/book/1163_\d+\.html'), callback='parse_item', follow=True),
    )

    # rules规则：包含了一个或者多个Rule对象，每个Rule对象对爬取网站的动作定义特定的操作，即：根据LinkExtractor里面的内容去匹配网页的url，然后取请求这个url，得到相应以后回调parse_item这个方法，进行处理
    # LinkExtractor：是一个link匹配的对象，可以根据里面规则去提取链接
    # callback：回调函数，【注意】crawlspider里面回调函数要用字符串来传

    # 【LinkExtractor的规则】
    # 1）用正则匹配 LinkExtractor(allow=r"某规则")
    # 2）用xpath匹配 LinkExtractor(restrict_xpaths="某xpath语法规则")
    # 3）用css匹配 LinkExtractor(restrict_css="某css选择器")

    def parse_item(self, response):
        # 提取出所有的书籍
        booklist = response.xpath("//div[@class='bookslist']/ul/li")
        # print(len(booklist))
        for book in booklist:
            item = CrawlspiderdemoItem()
            item["title"] = book.xpath(".//h3/a/text()").extract_first()
            item["author"] = book.xpath(".//p[1]/a/text()").extract_first()

            item["info"] = book.xpath(".//p[2]/text()").extract_first()
            item["img_url"] = book.xpath(".//img/@data-original").extract_first()
            yield item



    # return ["12","12"]
