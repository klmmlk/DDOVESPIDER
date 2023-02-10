import scrapy
from scrapy.http import HtmlResponse
from config import COOKIES


class DdoveSpider(scrapy.Spider):
    name = "ddove"
    allowed_domains = ["ddove.com"]
    start_urls = ["http://ddove.com/data/list_2__0_0_1__1.0-2.0-3.13_1.html"]

    def __init__(self):
        super(DdoveSpider, self).__init__()
        self.cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in COOKIES.split('; ')}

    def parse(self, response: HtmlResponse):
        node_list = response.xpath('//div[@class="dlisttitle"]/a[1]/@href')
        for node in node_list:
            url = node.get()
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):
        downpage_url = response.urljoin(response.xpath('//div[@class="rdown"]/a[1]/@href').get())
        yield scrapy.Request(downpage_url, callback=self.page_detail, cookies=self.cookies_dict)

    # 获取标题、图片、下载地址
    def page_detail(self, response: HtmlResponse):
        dl_url = response.urljoin(response.xpath('//a[@class="filedownlink"]/@href').get())
        print(dl_url)
