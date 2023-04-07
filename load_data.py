'''
Author: sun510001 sqf121@gmail.com
Date: 2023-04-07 15:31:53
LastEditors: sun510001 sqf121@gmail.com
LastEditTime: 2023-04-07 17:07:33
FilePath: /spider_for_luxun_text/load_data.py
Description: 
'''
import json
import os
import re
import random


def load_json(path):
    """读取json文件

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(path, 'r', encoding='utf-8') as fp:
        data_list = json.load(fp)
    return data_list


def main():
    output_dir = "data_dir"
    result_file = os.path.join(output_dir, "luxun.json")

    text_list = load_json(result_file)

    # 统计爬到的文章数量和总字数
    word_sum = 0
    for text in text_list:
        pattern = re.compile(r'[\u4e00-\u9fa5]')
        word_sum += len(pattern.findall(text[-1]))

    print(f"共有文章: {len(text_list)}条. 共{word_sum}字.")
    
    title_list = []
    for text in text_list:
        title_list.append(text[:-1])
        
    # data = load_json(os.path.join(output_dir, "luxun.json"))
    # for each in data:
    #     print(each[:-1])

    # 随机抽取5篇内容打印出来
    limit = 5
    r_index_list = random.sample(range(len(text_list)), limit)

    for index in r_index_list:
        info = " ".join(text_list[index][:-1])

        print(f"\n现提取第篇{index}文章")
        if info:
            print(f"info: {info}\n")
        text = text_list[index][-1]

        print(text, "\n")


if __name__ == "__main__":
    main()
