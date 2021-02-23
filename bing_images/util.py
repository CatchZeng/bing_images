import requests
import shutil
import posixpath
import urllib
import os

def download_image(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def file_name(url, index, prefix = 'image') -> str:
    try:
        path = urllib.parse.urlsplit(url).path
        filename = posixpath.basename(path).split('?')[0]
        file_type = filename.split(".")[-1]
        if file_type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
            file_type = "jpg"
        result = "{}_{}.{}".format(prefix, str(index), file_type)
        return result
    except Exception as e:
        print("[!] Issue getting: {}\n[!] Er = 0ror:: {}".format(url, e))
        return prefix

DEFAULT_OUTPUT_DIR = "bing-images"

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