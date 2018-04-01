__all__ = ["download", "get_clipboard", "file_append_if_not", "save_image", "make_parent_dir", "save_data", "save_url"]

import os
import errno
from urllib.request import urlopen
from logging import info
import random
import string
import logging
import subprocess

_gen_random_string_options_ = string.ascii_uppercase + string.ascii_lowercase + string.digits


def get_clipboard():
    p = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
    p.wait()
    data = p.stdout.read()
    return data.decode(encoding="utf-8")


def download(URL, PATH):
    make_parent_dir(PATH)

    #info("Downloading: %s to %s" % (URL, PATH))
    devnull = open('/dev/null', 'w')
    process = subprocess.Popen(['wget', '--continue', '-O', PATH, URL], stdout=devnull, stderr=devnull)

    process.wait()


def file_append_if_not(path, text):
    found = False
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if text in line:
                    found = True
    if not found:
        with open(path, 'a+') as f:
            f.write(text + "\n")
    return found


def save_image(response, path):
    # Save image
    save_data(path, response.body)

    # Send image item(for the item count)
    #yield Image(url=response.url, path=path)


def gen_random(length=20):
    return ''.join(random.choices(_gen_random_string_options_, k=length))


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def make_parent_dir(file_path):
    # If parent folders don't exist create them
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def save_data(file_path, data):
    # If parent folders don't exist create them
    make_parent_dir(file_path)

    # Write data to file
    with open(file_path, 'wb') as f:
        f.write(data)


def move(src, dist):
    make_parent_dir(dist)
    os.rename(src, dist)


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
    return Image(url=url, path=path)

