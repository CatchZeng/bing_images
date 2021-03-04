try:
    from util import get_file_name, rename, make_image_dir, download_image
except ImportError:  # Python 3
    from .util import get_file_name, rename, make_image_dir, download_image
from typing import Counter, List
from multiprocessing.pool import ThreadPool
from time import time as timer
import requests
import re
import os

FETCH_IMAGE_URL = "https://www.bing.com/images/async"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}


class Bing:
    def fetch_image_urls(
        self,
        query: str,
        first: int = 0,
        count: int = 20,
        adult: bool = False,
        filters: str = "",
    ) -> List[str]:
        params = {
            "q": query,
            "first": first,
            "count": count,
            "adlt": adult,
            "qft": filters,
        }
        try:
            r = requests.get(FETCH_IMAGE_URL, headers=HEADERS, params=params)
            r.raise_for_status()
        except Exception as exc:
            print(exc)
            raise exc

        try:
            urls = re.findall(r"murl&quot;:&quot;(.*?)&quot;", r.text)
        except Exception as exc:
            print(exc)
            raise exc

        return urls


def fetch_image_urls(
    query: str,
    limit: int = 20,
    adult: bool = False,
    file_type: str = "jpg",
    filters: str = '',
    max_page_counter: int = 10
) -> List[str]:
    result = list()
    page_counter = 0

    bing = Bing()
    while len(result) < limit:
        urls = bing.fetch_image_urls(
            query, page_counter, limit, adult, file_type + filters)
        for url in urls:
            if url.endswith(file_type):
                result.append(url)
                if len(result) >= limit:
                    break
        page_counter += 1
        if page_counter >= max_page_counter:
            break
    return result


def download_images(
    query: str,
    limit: int = 20,
    output_dir='',
    pool_size: int = 20,
    adult: bool = False,
    file_type: str = "jpg",
    filters: str = '',
    force_replace=False
):
    start = timer()
    image_dir = make_image_dir(output_dir, force_replace)
    print("Save path: {}".format(image_dir))

    urls = fetch_image_urls(query, limit, adult, file_type, filters)
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
    download_images("cat", 20, output_dir="/Users/catchzeng/Desktop/cat", pool_size=10,
                    file_type="jpg", force_replace=True)
