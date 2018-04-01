from .file import make_parent_dir, save_data
from .misc import gen_random, sizeof_fmt
import os
from multiprocessing import Process
import logging
from urllib.request import urlopen


def download(URL, PATH):
    if os.path.exists(PATH):
        return

    make_parent_dir(PATH)

    # Download file to tmp
    TMP = os.path.join(os.path.dirname(PATH), ".download." + gen_random())
    while os.system("wget --read-timeout=20 -O %s %s" % (TMP, URL)) != 0:
        os.remove(TMP)

    # Move to destination
    os.rename(TMP, PATH)


def save_image(response, path):
    # Save image
    save_data(path, response.body)

    # Send image item(for the item count)
    #yield Image(url=response.url, path=path)


def save_url(url, path, tmp_dir=".tmp", block_sz=1024 * 500):
    site = urlopen(url)
    file_size = int(site.info()["Content-Length"])

    # Check if file is bigger than current
    if os.path.exists(path):
        local_file_size = os.stat(path).st_size

        if local_file_size >= file_size:
            return None
        logging.debug("Remote file is bigger than local")

    logging.debug("Downloading: {0!s}".format(url))

    # TMP file directory
    tmp = os.path.join(tmp_dir, gen_random())
    make_parent_dir(tmp)

    # Download
    with open(tmp, "wb") as f:
        file_size_dl = 0
        while True:
            buffer = site.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)

            f.write(buffer)

            status = r"%s  [%3.2f%%]" % (sizeof_fmt(file_size_dl), file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            logging.debug(status)
        f.close()

    # Move
    make_parent_dir(path)
    os.rename(tmp, path)

    # Return Item
    # return Image(url=url, path=path)


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
