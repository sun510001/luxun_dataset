'''
Author: sun510001 sqf121@gmail.com
Date: 2023-04-07 15:31:53
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2023-04-07 17:07:33
FilePath: /spider_for_luxun_text/spider_test.py
Description: 爬取北京鲁迅博物馆网页中鲁迅的文章数据
             单个ip存在访问次数限制每天访问不要超过1w次
             访问链接的间隔建议大于1s
'''
import os
import requests
import time
import json
import random

from bs4 import BeautifulSoup


def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def extract_links_first(soup):
    links = []
    for link in soup.find_all('a'):
        url = link.get('href')
        if url and 'lid' in url and [[], url] not in links:
            # 如果网址中有lid, 并且这个网址不存在于列表, 保存
            links.append([[], url])

    return links


def extract_links(table_list):
    """从table中找到的链接列表

    Args:
        table_list (_type_): _description_

    Returns:
        _type_: _description_
    """
    links = []
    for l in table_list:
        if 'php?' in l[-1]:
            links.append([l[:-1], l[-1]])
    return links


def find_next_page(soup):
    """查看这一页是否存在下一页按钮

    Args:
        soup (_type_): _description_
    """
    np_result = soup.find('div', class_='fanye')
    if np_result:
        page_url_list = extract_links_first(np_result)
    else:
        page_url_list = None
    return page_url_list


def extract_table_data(soup):
    """查找table元素

    Args:
        soup (_type_): _description_

    Returns:
        _type_: _description_
    """
    table_data = []
    table = soup.find('table')

    if table:
        rows = table.find_all('tr')
        for row in rows:
            row_data = []
            columns = row.find_all(['td', 'th'])
            for column in columns:
                text = column.get_text().strip()
                row_data.append(text)

                # 如果最后一列是超链接
                if column == columns[-1]:
                    link = column.find('a')
                    if link:
                        href = link.get('href')
                        row_data.append(href)

            table_data.append(row_data)

    return table_data


def find_content(soup):
    """设定爬取内容所在的元素

    Args:
        soup (_type_): _description_

    Returns:
        _type_: _description_
    """
    content = soup.find('div', class_='ctcontent')
    return content


def get_random_number(min, max):
    random_number = random.uniform(min, max)
    return random_number


def crawl_website(output_path, start_url, max_depth=20, delay_min=1, delay_max=3):
    """爬取网页数据, 可以定义爬取深度, 起始网址和每次访问之间的等待时间

    Args:
        output_path (_type_): 输出文件夹地址
        start_url (_type_): 起始的网址
        max_depth (int, optional): 爬取深度. Defaults to 20.
        delay_min (float, optional): 每次访问之间的等待时间最小值(单位s). Defaults to 1.
        delay_max (float, optional): 每次访问之间的等待时间最大值(单位s). Defaults to 3.
    """
    visited_urls = set()  # 已经访问过的网址, 防止重复访问
    crawl_queue = [[[], start_url, 0]]
    save_content_list = []
    table_data_list = []
    first_load = True  # 第一页没有table数据, 需要将所有链接先都过一遍

    while crawl_queue:
        content_list, url, depth = crawl_queue.pop(0)
        tmp_content_list, tmp_url, tmp_depth = content_list, url, depth
        if url not in visited_urls and depth <= max_depth:
            visited_urls.add(url)

            if url != start_url:
                url = '/'.join(start_url.split("/")[:-1]) + '/' + url

            print(f'Visiting: {url}')
            try:
                soup = get_soup(url)

                content = find_content(soup)
                if content:
                    # 如果找到了内容, 就把内容添加到列表
                    content_list = [x for x in content_list if '查看正文' not in x]
                    save_content_list.append(
                        content_list + [content.get_text()])

                if not first_load:
                    table_data_list = extract_table_data(soup)

                delay = get_random_number(delay_min, delay_max)
                time.sleep(delay)

                if depth <= max_depth:
                    if not first_load:
                        links = extract_links(table_data_list)
                        # 查看页面中有没有翻页按钮, 有的话找出翻页的网址列表
                        next_page_url = find_next_page(soup)
                        if next_page_url is not None:
                            links.extend(next_page_url)
                    else:
                        links = extract_links_first(soup)
                        first_load = False

                    for link in links:
                        crawl_queue.append(link + [depth + 1])
            except Exception as e:
                print(f'Error: {e}')
                print(f"try {tmp_url} again...")
                time.sleep(2)
                if tmp_url in visited_urls:
                    del visited_urls[tmp_url]
                    crawl_queue.append([tmp_content_list, tmp_url, tmp_depth])

    with open(output_path, "w", encoding='utf-8') as fp:
        json.dump(save_content_list, fp, ensure_ascii=False)


def main():
    output_dir = "data_dir"
    os.makedirs(output_dir, exist_ok=True)
    result_file = os.path.join(output_dir, "luxun.json")

    start_url = 'http://www.luxunmuseum.com.cn/cx/works.php'
    crawl_website(result_file, start_url)


if __name__ == "__main__":
    main()
