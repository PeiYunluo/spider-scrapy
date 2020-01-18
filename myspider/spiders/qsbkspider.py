# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
from myspider.items import MyspiderItem


# /html/body/div[3]/div/div[2]/div[1]/div[2]

class QsbkspiderSpider(scrapy.Spider):
    name = 'qsbkspider'
    allowed_domains = ['budejie.com/']
    start_urls = ['http://www.budejie.com/text/1']

    def parse(self, response):
        jrlist = response.xpath("//div[@class='j-r-list']/ul/li")
        print("************************************************************")
        print(type(jrlist))
        print("************************************************************")
        for jrlistli in jrlist:
            author = jrlistli.xpath(".//div[@class='j-list-user']//div[@class='u-txt']//a/text()").get()
            content = jrlistli.xpath(".//div[@class='j-r-list-c']//div[@class='j-r-list-c-desc']//a/text()").get()
            # print(f"author:{author}")
            # print(f"content:{content}")
            item = MyspiderItem(author=author, content=content)
            # duanzi = {"author":author,"content":content}
            # print(duanzi)
            print(item)
            yield item
        next_url = response.xpath("//div[@class='j-page']//a[@class='pagenxt']/@href").get()
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        next_url_full = "http://www.budejie.com/text/"+ next_url
        print(next_url_full)
        print(int(next_url))
        if int(next_url)>=50:
            return
        else:
            yield scrapy.Request(next_url_full,callback=self.parse, dont_filter=True)
