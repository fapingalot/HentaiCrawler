from scrapy import Request, Spider
from ..items import Post


class XCartXSpider(Spider):
    name = "xcartx"

    def __init__(self, name=None, *args, **kwargs):
        self.name = name

        # Superclass constructor
        super(XCartXSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        name = self.name

        if name:
            yield Request("http://xcartx.com/"+name+".html", self.parse)

    def parse(self, response):
        comic = Post(
            title=response.xpath("//title/text()").extract_first().strip(),
            id=self.name,
            url=response.url,
            content=[]
        )

        for c in response.css(".full-story tr > td > div > img,a"):
            page = c.xpath("@src").extract() + c.xpath("@href").extract()
            comic['content'] += [response.urljoin(p) for p in page if "/uploads/posts/" in p]

        yield comic
