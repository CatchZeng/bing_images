from urllib.parse import quote
import shutil
from selenium import webdriver
import time
import json

BASE_URL = "https://www.bing.com/images/search?"


def gen_query_url(keywords, filters, extra_query_params =''):
    keywords_str = "&q=" + quote(keywords)
    query_url = BASE_URL + keywords_str
    if len(filters) > 0:
        query_url += "&qft="+filters
    query_url += extra_query_params
    return query_url


def image_url_from_webpage(driver, max_number=10000):
    image_urls = list()

    time.sleep(10)
    img_count = 0

    while True:
        image_elements = driver.find_elements_by_class_name("iusc")
        if len(image_elements) > max_number:
            break
        if len(image_elements) > img_count:
            img_count = len(image_elements)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
        else:
            smb = driver.find_elements_by_class_name("btn_seemore")
            if len(smb) > 0 and smb[0].is_displayed():
                smb[0].click()
            else:
                break
        time.sleep(3)
    for image_element in image_elements:
        m_json_str = image_element.get_attribute("m")
        m_json = json.loads(m_json_str)
        image_urls.append(m_json["murl"])
    return image_urls


def crawl_image_urls(keywords, filters, max_number=10000, proxy=None, proxy_type="http", extra_query_params =''):
    chrome_path = shutil.which("chromedriver")
    chrome_path = "./bin/chromedriver" if chrome_path is None else chrome_path
    chrome_options = webdriver.ChromeOptions()
    if proxy is not None and proxy_type is not None:
        chrome_options.add_argument(
            "--proxy-server={}://{}".format(proxy_type, proxy))
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

    query_url = gen_query_url(keywords, filters, extra_query_params)
    driver.set_window_size(1920, 1080)
    driver.get(query_url)
    image_urls = image_url_from_webpage(driver, max_number)
    driver.close()

    if max_number > len(image_urls):
        output_num = len(image_urls)
    else:
        output_num = max_number

    print("Crawled {} image urls.".format(
        len(image_urls)))

    return image_urls[0:output_num]


if __name__ == '__main__':
    images = crawl_image_urls(
        "mbot png", "+filterui:aspect-square", max_number=10)
    for i in images:
        print(i+"\n")
