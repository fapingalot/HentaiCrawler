from scrapy import Request, Spider
from ..items import Post


class ThatPervertSpider(Spider):
    name = "thatpervert"

    def __init__(self, tag=None, *args, **kwargs):
        self.tag = tag

        # Superclass constructor
        super(ThatPervertSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        tag = self.tag

        if tag:
            yield Request("http://thatpervert.com/tag/"+tag, self.parse)

    def parse(self, response):
        # Iterate for every post on page
        for post in response.css(".postContainer"):
            _post = Post(
                title=response.xpath("//title/text()").extract_first().split("::")[0].split("/")[0].strip(),
                id=post.xpath("@id").extract_first().strip(),
                url=response.url,
                content=[],
                container="tag/"+self.tag if self.tag else response.url.split('/')[4]
            )

            # Extract image URLs from post
            links = post.css(".image").xpath("a/@href | img/@src | video/@src").extract()
            _post['content'] += [response.urljoin(link) for link in links if "post/" in link]

            yield _post

        # Go to next page if link exists
        next_page = response.css(".next").xpath("@href")
        if not len(next_page) == 0:
            yield response.follow(next_page.extract_first(), self.parse)
