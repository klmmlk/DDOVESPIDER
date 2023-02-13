import scrapy
from scrapy.http import HtmlResponse
from config import COOKIES
# from ddove_spider.items import DdoveSpiderItem
import re

from sql_ctr import MySql


class DdoveSpider(scrapy.Spider):
    name = "ddove"
    allowed_domains = ["ddove.com"]
    start_urls = ["http://ddove.com/data/list_2__0_0_1__1.0-2.0-3.13_1.html"]  # dwg

    # start_urls = ["http://ddove.com/data/list_2__0_0_1__1.0-2.0-3.16_1.html"]  # skp
    # start_urls = ["http://ddove.com/data/list_2__0_0_1__1.0-2.0-3.17_1.html"]  # ppt

    def __init__(self):
        super(DdoveSpider, self).__init__()
        self.cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in COOKIES.split('; ')}

    def parse(self, response: HtmlResponse):
        node_list = response.xpath('//div[@class="dlisttitle"]/a[1]/@href')
        for node in node_list:
            url = node.get()
            url_id = re.search(r'(?<=/)\w+(?=\.html)', url).group()
            # 在数据库中对比是否已爬取过
            if not MySql.search_db(url_id):
                item = {"url_id": url_id}
                if 'htmldatanew' in url:
                    yield scrapy.Request(url, callback=self.parse_newpage, meta={'item': item})
                else:
                    yield scrapy.Request(url, callback=self.parse_oldpage, meta={'item': item})
        # 模拟翻页
        part_url = response.xpath('//a[@class="nextpage"]/@href').get()
        if part_url:
            next_page = response.urljoin(part_url)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_newpage(self, response: HtmlResponse):
        item: dict = response.meta['item']
        title = response.xpath('//h1[@class="datatitle"]/text()').get()
        pic_list = response.xpath('//div[@class="conthumbbox"]/img/@src').extract()
        item.update({"title": title, "pic_url": pic_list})
        downpage_url = response.urljoin(response.xpath('//div[@class="rdown"]/a[1]/@href').get())
        yield scrapy.Request(downpage_url, callback=self.page_detail, cookies=self.cookies_dict,
                             meta={"item": item})

    def parse_oldpage(self, response: HtmlResponse):
        item: dict = response.meta['item']
        title = response.xpath('//h1/text()').get()
        pic_list = response.xpath('//div[@class="thumbbox"]/a/@href').extract()
        item.update({"title": title, "pic_url": pic_list})
        downpage_url = response.urljoin(response.xpath('//div[@class="extfiles"]/a/@href').get())
        yield scrapy.Request(downpage_url, callback=self.oldpage_detail, cookies=self.cookies_dict,
                             meta={"item": item})

    # 获取标题、图片、下载地址
    def page_detail(self, response: HtmlResponse):
        item: dict = response.meta['item']
        download_list = response.xpath('//a[@class="filedownlink"]/@href').extract()
        for i, k in enumerate(download_list):
            download_list[i] = response.urljoin(k)
        item['dl_url'] = download_list
        yield item

    def oldpage_detail(self, response: HtmlResponse):
        item: dict = response.meta['item']
        download_list = response.xpath('//table[@class="downfile"]/tr/td[5]/a[1]/@href').extract()
        for i, k in enumerate(download_list):
            download_list[i] = response.urljoin(k)
        item['dl_url'] = download_list
        yield item
