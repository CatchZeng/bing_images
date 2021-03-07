import requests
import shutil
import posixpath
import urllib
import os

DEFAULT_OUTPUT_DIR = "bing-images"


def download_image(url, path) -> bool:
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            return True
        else:
            print("[!] Download image: {}\n[!] Err :: {}".format(
                url, r.status_code))
            return False
    except Exception as e:
        print("[!] Download image: {}\n[!] Err :: {}".format(url, e))
        return False


def get_file_name(url, index, prefix='image') -> str:
    try:
        path = urllib.parse.urlsplit(url).path
        filename = posixpath.basename(path).split('?')[0]
        type, _ = file_data(filename)
        result = "{}_{}.{}".format(prefix, index, type)
        return result
    except Exception as e:
        print("[!] Get file name: {}\n[!] Err :: {}".format(url, e))
        return prefix


def rename(name, index, prefix='image') -> str:
    try:
        type, _ = file_data(name)
        result = "{}_{}.{}".format(prefix, index, type)
        return result
    except Exception as e:
        print("[!] Rename: {}\n[!] Err :: {}".format(name, e))
        return prefix


def file_data(name):
    try:
        type = name.split(".")[-1]
        name = name.split(".")[0]
        if type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
            type = "jpg"
        return (type, name)
    except Exception as e:
        print("[!] Issue getting: {}\n[!] Err :: {}".format(name, e))
        return (name, "jpg")


def make_image_dir(output_dir, force_replace=False) -> str:
    image_dir = output_dir
    if len(output_dir) < 1:
        image_dir = os.path.join(os.getcwd(), DEFAULT_OUTPUT_DIR)

    if force_replace:
        if os.path.isdir(image_dir):
            shutil.rmtree(image_dir)
    try:
        if not os.path.isdir(image_dir):
            os.makedirs(image_dir)
    except:
        pass

    return image_dir


if __name__ == '__main__':
    print("util")
