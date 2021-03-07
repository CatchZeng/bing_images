try:
    from util import get_file_name, rename, make_image_dir, download_image
except ImportError:  # Python 3
    from .util import get_file_name, rename, make_image_dir, download_image
try:
    from crawler import crawl_image_urls
except ImportError:  # Python 3
    from .crawler import crawl_image_urls
from typing import Counter, List
from multiprocessing.pool import ThreadPool
from time import time as timer
import os
import math


def fetch_image_urls(
    query: str,
    limit: int = 20,
    file_type: str = "jpg",
    filters: str = ''
) -> List[str]:
    result = list()
    keywords = query + " " + file_type
    max_number = math.ceil(limit*1.5)
    urls = crawl_image_urls(keywords, filters, max_number)
    for url in urls:
        if url.endswith(file_type) and url not in result:
            result.append(url)
            if len(result) >= limit:
                break
    return result


def download_images(
    query: str,
    limit: int = 20,
    output_dir='',
    pool_size: int = 20,
    file_type: str = "jpg",
    filters: str = '',
    force_replace=False
):
    start = timer()
    image_dir = make_image_dir(output_dir, force_replace)
    print("Save path: {}".format(image_dir))

    urls = fetch_image_urls(query, limit, file_type, filters)
    entries = get_image_entries(urls, image_dir)

    print("Downloading images")
    ps = pool_size
    if limit < pool_size:
        ps = limit
    download_image_entries(entries, ps)

    rename_images(image_dir, query)

    print("Done")
    elapsed = timer() - start
    print("Elapsed time: %.2fs" % elapsed)


def rename_images(dir, prefix):
    files = os.listdir(dir)
    index = 1
    print("Renaming images")
    for f in files:
        if f.startswith("."):
            print("Escape {}".format(f))
            continue
        src = os.path.join(dir, f)
        name = rename(f, index, prefix)
        dst = os.path.join(dir, name)
        os.rename(src, dst)
        index = index + 1
    print("Finished renaming")


def download_image_entries(entries, pool_size):
    counter = 1
    results = ThreadPool(pool_size).imap_unordered(
        download_image_with_thread, entries)
    for (url, result) in results:
        if result:
            print("#{} {} Downloaded".format(counter, url))
            counter = counter + 1


def get_image_entries(urls, dir):
    entries = []
    i = 0
    for url in urls:
        name = get_file_name(url, i, "#tmp#")
        path = os.path.join(dir, name)
        entries.append((url, path))
        i = i + 1
    return entries


def download_image_with_thread(entry):
    url, path = entry
    result = download_image(url, path)
    return (url, result)


if __name__ == '__main__':
    download_images("cat",
                    20,
                    output_dir="/Users/catchzeng/Desktop/cat",
                    pool_size=10,
                    file_type="png",
                    force_replace=True)
