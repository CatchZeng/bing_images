try:
    from util import file_name, make_image_dir, download_image
except ImportError:  # Python 3
    from .util import file_name, make_image_dir, download_image
from typing import List
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
    output_dir='dataset',
    processes: int = 20,
    adult: bool = False,
    file_type: str = "jpg",
    filters: str = '',
    force_replace=False
):
    image_dir = make_image_dir(output_dir, query, force_replace)

    urls = fetch_image_urls(query, limit, adult, file_type, filters)
    counter = 1
    print("Save path: {}".format(image_dir))
    entries = []
    for url in urls:
        name = file_name(url, counter, query)
        path = os.path.join(image_dir, name)
        entries.append((url, path))
        counter += 1

    start = timer()

    tp =  processes
    if limit < processes:
        tp = limit
    results = ThreadPool(tp).imap_unordered(download_image_with_thread, entries)
    for path in results:
        print("Downloaded", path)

    print("Done")
    print(f"Elapsed Time: {timer() - start}")


def download_image_with_thread(entry):
    url, path = entry
    print("Downloading {} from {}".format(path, url))
    download_image(url, path)
    return path


if __name__ == '__main__':
    # urls = fetch_image_urls("cat", limit=100, file_type='png',
    #                         filters='+filterui:aspect-square+filterui:color2-bw')
    # print("{} images.".format(len(urls)))
    # counter = 1
    # for url in urls:
    #     print("{}: {}".format(counter, url))
    #     counter += 1
    download_images("cat", 20, file_type="png", force_replace=True)
