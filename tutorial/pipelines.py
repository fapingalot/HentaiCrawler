from os.path import join

from .spiders.xcartx import XCartXSpider
from .spiders.shadebase import ShadbaseSpider
from .spiders.thatpervert import ThatPervertSpider
from .spiders.simplyhentai import SimplyHentaiSpider

# from .util.file import create_sysln
from .util.url import Downloader
import os


class ImagePipeline(object):
    BASE_PATH = os.environ["S_OUT_DIR"] if "S_OUT_DIR" in os.environ else "data/"
    downloader = Downloader()

    def process_item(self, item, spider):
        if type(spider) is XCartXSpider:
            self.xcrart(item)
        elif type(spider) is ShadbaseSpider:
            self.shadbase(item)
        elif type(spider) is ThatPervertSpider:
            self.that_pervert(item)
        elif type(spider) is SimplyHentaiSpider:
            self.simply_hentai(item)

    def xcrart(self, item):
        base = join(self.BASE_PATH, "XCartX")

        #create_sysln(join("..", item['id']), join(base, '.names/', item['title']))
        self.downloader.download_numbered(item["content"], join(base, item['id']), single=False)

    def simply_hentai(self, item):
        base = join(self.BASE_PATH, "SimplyHentai")

        path = join(base, item["container"], item['id'])

        link_path = join(path, '../.names/', item['title'])
        #create_sysln(join("..", item['id']), link_path)

        self.downloader.download_numbered(item['content'], path, single=False)

    def that_pervert(self, item):
        base = join(self.BASE_PATH, "ThatPervert")

        #create_sysln(join("..", item['container']), join(base, '.names/', item['title']))
        self.downloader.download_numbered(item['content'], join(base, item['container'], item['id']))

    def shadbase(self, item):
        base = join(self.BASE_PATH, "Shadebase")

        self.downloader.download_numbered(item['content'], join(base, item['id']))
