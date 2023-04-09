# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import re

import pandas as pd

class ExportMovieDetail:
    def __init__(self) -> None:
        head = pd.DataFrame(columns=['title', "rating","score_num", "comment_num",'weight','id',"url"])
        head.to_csv('detail.csv')
        pass

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        title = item.get("title", "[title]")
        rating=item.get("rating","")
        score_num=item.get("score_num","")
        comment_num=item.get("comment_num","")
        url = item.get("url", "[url]")
        id = item.get("id", "[id]")

        regex=re.compile('[0-9]+')

        comment_num=regex.findall(comment_num)[0]

        weight=round(float(comment_num)/float(score_num),3)
        df = pd.DataFrame([[title, rating,score_num,comment_num,weight,id,url]])

        df.to_csv("detail.csv", header=False, mode="a",encoding="gbk")
        
        return item
