import scrapy
from scrapy.http import HtmlResponse


class DdoveSpider(scrapy.Spider):
    name = "ddove"
    allowed_domains = ["ddove.com"]
    start_urls = ["http://ddove.com/data/list_2__0_0_1__1.0-2.0-3.13_1.html"]

    def parse(self, response: HtmlResponse):
        node_list = response.xpath('//div[@class="dlisttitle"]/a[1]/@href')
        for node in node_list:
            url = node.get()
            yield scrapy.Request(url,callback=self.parse_page)

    def parse_page(self,response:HtmlResponse):
        downpage_url = response.urljoin(response.xpath('//div[@class="rdown"]/a[1]/@href').get())
        print(downpage_url)
        pass

    def page_detail(self,response:HtmlResponse):

        pass