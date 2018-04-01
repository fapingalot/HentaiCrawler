from scrapy import Request, Spider
from ..items import Post


class ShadbaseSpider(Spider):
    name = "shadbase"

    def start_requests(self):
        yield Request("http://www.shadbase.com/category/archiveall/", self.parse)

    def parse(self, response):
        # Parse all posts on page
        for post in response.css(".comicthumbwrap a").xpath("@href").extract():
            yield response.follow(post, self.parse_post)

        # Go to next page if link exists
        for next_page in response.css(".paginav-next a").xpath("@href").extract():
            yield response.follow(next_page, self.parse)

    def parse_post(self, response):
        post = Post(
            title=response.xpath("//title/text()").extract_first().split(' | ')[0].strip(),
            id=response.url.split("/")[3].lstrip("/").strip(),
            url=response.url,
            content=[]
        )

        for comic in response.css("#comic div"):
            for link in comic.css("image,img,video").xpath("@src").extract():
                post['content'].append(response.urljoin(link))
            for link in comic.css("object").xpath("@data").extract():
                post['content'].append(response.urljoin(link))

        yield post
