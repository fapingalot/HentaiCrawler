from scrapy import Request, Spider
from ..items import Post


class SimplyHentaiSpider(Spider):
    name = "simplyhentai"

    def __init__(self, series=None, name=None, *args, **kwargs):
        self.series = series
        self.name = name

        # Superclass constructor
        super(SimplyHentaiSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        series = self.series
        name = self.name

        if series and name:
            yield Request("https://www.simply-hentai.com/"+series+'/'+name, self.parse)

    def parse(self, response):
        if "/all-pages" not in response.url:
            yield Request(response.url+"/all-pages", self.parse)
            return

        comic = Post(
            title=response.xpath("//title/text()").extract_first().split("/")[0].strip(),
            id=self.name,
            url=response.url,
            content=[],
            container=self.series
        )

        pages = response.css(".block-with-frame > div > div > a")
        for page in pages:
            p = page.xpath("picture/source/@data-srcset").extract()[0]
            p = p.replace("/Album/", "/")                   \
                .replace("/very_small/", "/full/")          \
                .replace("/small/", "/full/")               \
                .replace("/thumb/", "/full/")

            comic['content'] += [p]

        yield comic
