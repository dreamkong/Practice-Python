import json
from json import JSONDecodeError
import re
import os
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient('localhost', connect=False)
db = client['toutiao']

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


def get_page_index(offset, keyword):
    data = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': True,
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    url = 'https://www.toutiao.com/api/search/content/'
    try:
        response = requests.get(url, params=data, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_page_index(html):
    data = json.loads(html)
    # print(data)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    images_pattern = re.compile('gallery:\sJSON.parse\((.*?)\),', re.S)
    result = re.search(images_pattern, html)
    if result:
        try:
            data = json.loads(json.loads(result.group(1)))
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item['url'] for item in sub_images]
                return {
                    'title': title,
                    'url': url,
                    'images': images
                }
        except JSONDecodeError:
            print('json解析错误~~')


def save_to_mongo(result):
    if db['jiepai'].insert(result):
        print('存储到MongoDB成功！', result.get('title'))
        return True
    return False


def download_image(result):
    base_file_path = os.getcwd() + '/街拍爬虫/' + result.get('title')
    if not os.path.exists(base_file_path):
        os.makedirs(base_file_path)
    for url in result.get('images'):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                file_path = base_file_path + '/' + url.split('/')[-1] + '.jpg'
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                continue
        except RequestException:
            continue


def main(offset, keyword='街拍'):
    html = get_page_index(offset, keyword)
    for url in parse_page_index(html):
        print(url)
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            if result:
                save_to_mongo(result)
                download_image(result)


GROUP_START = 1
GROUP_END = 5

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
