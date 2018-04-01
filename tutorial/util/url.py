from .file import make_parent_dir, save_data
from .misc import gen_random, sizeof_fmt
import os
from multiprocessing import Process
import logging
import time
from urllib.request import urlopen


def download(URL, PATH):
    if os.path.exists(PATH):
        return

    make_parent_dir(PATH)

    # Download file to tmp
    TMP = os.path.join(os.path.dirname(PATH), ".download." + gen_random())
    while os.system("curl %s -o %s --silent" % (URL, TMP)) != 0:
        logging.error("Failed to download file %s retrying..." % PATH)
        if os.path.exists(TMP):
            os.remove(TMP)

        time.sleep(10)

    # Move to destination
    os.rename(TMP, PATH)
    logging.info("Downloaded: %s" % PATH)


class Downloader:
    def __init__(self, limit=5):
        self.DOWNLOADS = []
        self.DOWNLOAD_LIMIT = limit

    def download(self, URL, PATH):
        PATH += '.' + URL.split('.')[-1]

        p = Process(target=download, args=(URL, PATH))
        p.start()
        self.DOWNLOADS += [p]

        while len(self.DOWNLOADS) > self.DOWNLOAD_LIMIT:
            self.DOWNLOADS = [x for x in self.DOWNLOADS if x.is_alive()]

    def download_numbered(self, URLs, PATH, single=True):
        if single and len(URLs) == 1:
            self.download(URLs[0], PATH)
        else:
            for i, img in enumerate(URLs):
                image_path = os.path.join(PATH, "{0:0>3}".format(i))
                self.download(img, image_path)
