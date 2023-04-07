# 鲁迅文章数据集
- 数据来源: http://www.luxunmuseum.com.cn/cx/works.php
- 共有文章: 3574条. 汉字共3129538字.
- 内容包括鲁迅的著作, 书信, 日记和专题. 数据未经过清洗.
- 数据集已经保存在`/data_dir/luxun.json`, 不需要再爬取.

## 数据获取的方法
```
python spider_test.py
```

## 读取数据的方法
```
# 随机读取5篇文章
python load_data.py
```