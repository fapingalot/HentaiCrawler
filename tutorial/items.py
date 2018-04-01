import scrapy


class Post(scrapy.Item):
    title = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()

    content = scrapy.Field()

    container = scrapy.Field()
