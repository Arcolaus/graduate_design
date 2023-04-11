# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pandas as pd

class ExportMovieDetail:
    def __init__(self) -> None:
        head = pd.DataFrame(columns=['title', "rating","score_num", "comment_num",'ratio','id'])
        head.to_csv('detail.csv',)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        title = item.get("title", "[title]")
        rating=item.get("rating","")
        score_num=item.get("score_num","")
        comment_num=item.get("comment_num","")
        id = item.get("id", "[id]")

        comment_num=comment_num[2:-2]
        ratio=round(float(comment_num)/float(score_num),3)

        df = pd.DataFrame([[title, rating,score_num,comment_num,ratio,id]])

        df.to_csv("detail.csv", header=False, mode="a")
        
        return item

class ExportMovieList:
    def __init__(self) -> None:
        head=pd.DataFrame(columns=['title',"id",'url'])
        head.to_csv('movie_list.csv')

    def process_item(self,item,spider):

        title=item.get("title","[title]")
        url=item.get("url","[url]")
        id=item.get("id","[id]")

        df=pd.DataFrame([[title,id,url]])
        df.to_csv("movie_list.csv",header=False,mode="a")

        return item
    
class ExportComments:
    def __init__(self) -> None:
        pass

    def open_spider(self,spider):
        # head=pd.DataFrame(columns=["id","title","score","stars","content"])
        # head.to_csv("contents.csv")
        pass

    def process_item(self,item,spider):

        title=item.get("movie_title","[title]")
        id=item.get("movie_id","[id]")
        score=item.get("score","[score]")
        stars=item.get("stars","[stars]")
        content=item.get("content","[content]")

        if len(score) == 16:
            score=score[7:8]
        else:
            score="[NULL]"

        df=pd.DataFrame([[id,title,score,stars,content]])
        df.to_csv("contents.csv",header=False,mode="a")

        return item
    
class ExportProxy:
    def __init__(self) -> None:
        pass

    def open_spider(self,spider):
        head=pd.DataFrame(columns=["ip","port","proxy_url"])
        head.to_csv("proxy_list.csv")
    
    def process_item(self,item,spider):
        re=r"http://((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}:[0-9]+"
        ip=item.get("ip","[ip]")
        port=item.get("port","[port]")
        proxy_url=item.get("proxy_url","[proxy_url]")

        df=pd.DataFrame([[ip,port,proxy_url]])
        df.to_csv("proxy_list.csv",header=False,mode="a")

        return item