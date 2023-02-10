# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DdoveSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 项目标题
    title = scrapy.Field()
    # 图片地址
    pic_url = scrapy.Field()
    # 下载地址
    download_url = scrapy.Field()

