# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pandas as pd


class ExportMovieList:
    def __init__(self) -> None:
        head=pd.DataFrame(columns=['title',"id",'url'])
        head.to_csv('movie_list.csv')
        pass

    def process_item(self,item,spider):

        title=item.get("title","[title]")
        url=item.get("url","[url]")
        id=item.get("id","[id]")

        df=pd.DataFrame([[title,id,url]])
        df.to_csv("movie_list.csv",header=False,mode="a")

        print("detail: {}".format(title))

        return item
    
class ExportMovieDetail:
    def __init__(self) -> None:
        head = pd.DataFrame(columns=['title', "rating","score_num", "comment_num",'ratio','id'])
        head.to_csv('movie_detail.csv',)
        pass

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
    
class ExportComments:
    def __init__(self) -> None:
        pass

    def open_spider(self,spider):
        # head=pd.DataFrame(columns=["id","title","score","stars","content"])
        # head.to_csv("contents.csv",index=False)
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
        df.to_csv("contents.csv",header=False,mode="a",index=False)

        # print("content: {}".format(content))

        return item

# ==================================split line=================================

class ExportCeleWorksList:
    def __init__(self) -> None:
        head=pd.DataFrame(columns=['title',"id",'url'])
        head.to_csv('cele_works.csv')

    def close_spider(self,spider):
        df=pd.read_csv("cele_works.csv")
        df.drop_duplicates(subset=["id"],inplace=True)
        df.drop(df.columns[0],axis=1,inplace=True)
        df.to_csv("cele_works.csv",columns=['title',"id",'url'])
        pass

    def process_item(self,item,spider):
        
        # if item == None:
        #     return None

        title=item.get("title","[title]")
        url=item.get("url","[url]")
        id=item.get("id","[id]")

        df=pd.DataFrame([[title,id,url]])

        df.to_csv("cele_works.csv",header=False,mode="a")

        return item
    
class ExportCeleWorksDetail:
    def __init__(self) -> None:
        head = pd.DataFrame(columns=['title', "rating","score_num", "comment_num",'ratio','id'])
        head.to_csv('tmp_cele_works_detail.csv')
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self,spider):
        df=pd.read_csv("tmp_cele_works_detail.csv")
        df.drop(df.columns[0],axis=1,inplace=True)
        df.to_csv("cele_detail.csv",columns=['title', "rating","score_num", "comment_num",'ratio','id'])
        

    def process_item(self, item, spider):

        title = item.get("title", "[title]")
        rating=item.get("rating","")
        score_num=item.get("score_num","")
        comment_num=item.get("comment_num","")
        id = item.get("id", "[id]")

        comment_num=comment_num[2:-2]
        ratio=round(float(comment_num)/float(score_num),3)

        df = pd.DataFrame([[title, rating,score_num,comment_num,ratio,id]])

        df.to_csv("cele_works_detail.csv", header=False, mode="a")
        
        return item

class ExportCeleComments:
    def __init__(self) -> None:
        pass

    def open_spider(self,spider):
        head=pd.DataFrame(columns=["id","title","score","stars","content"])
        head.to_csv("cele_comments.csv")
        pass

    def close_spider(self,spider):
        df=pd.read_csv("cele_comments.csv",on_bad_lines="skip")
        df.drop(df[df['score']=="[NULL]"].index,inplace=True)
        df.drop(df.columns[0],axis=1,inplace=True)
        df.to_csv("cele_comments.csv",columns=["id","title","score","stars","content"])

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
        df.to_csv("cele_comments.csv",header=False,mode="a")

        print("title: {}".format(title))

        return item 

class ExportMLWorkDetail:
    def __init__(self) -> None:
        pass

    def open_spider(self,spider):
        head=pd.DataFrame(columns=["title","work_id","score_num","watched_num","comment_num","ratio"])
        head.to_csv("tmp_ml_work_detail.csv")
    
    def close_spider(self,spider):
        df=pd.read_csv("tmp_ml_work_detail.csv")
        df.drop(df.columns[0],axis=1,inplace=True)
        df.to_csv("ml_work_detail.csv",index=False)

    def process_item(self,item,spider):
        title=item.get("title","[title]")
        work_id=item.get("work_id","[work_id]")
        score_num=item.get("score_num","[score_num]")
        comment_num=item.get("comment_num","[comment_num]")
        watched_num=item.get("watched_num","[watched_num]")

        comment_num=comment_num[2:-2]
        ratio=float(comment_num)/float(score_num)

        df=pd.DataFrame([[title,work_id,score_num,watched_num,comment_num,ratio]])
        df.to_csv("tmp_ml_work_detail.csv",header=False,mode="a")

        return item

class ExportRatingRatio:
    def __init__(self) -> None:
        pass

    def open_spider(self,spider):
        head=pd.DataFrame(columns=["title","work_id","5star_ratio","4star_ratio","3star_ratio","2star_ratio","1star_ratio"])
        head.to_csv("rating_ratio.csv")
    
    def close_spider(self,spider):
        df=pd.read_csv("rating_ratio.csv")
        df.drop(df.columns[0],axis=1,inplace=True)
        df.to_csv("rating_ratio.csv",index=False)

    def process_item(self,item,spider):
        title=item.get("title","[]")
        work_id=item.get("work_id","[]")
        score_num=item.get("score_num","[]")
        ratio_5s=item.get("ratio_5s","[]")
        ratio_4s=item.get("ratio_4s","[]")
        ratio_3s=item.get("ratio_3s","[]")
        ratio_2s=item.get("ratio_2s","[]")
        ratio_1s=item.get("ratio_1s","[]")
        
        df=pd.DataFrame([[title,work_id,score_num,ratio_5s,ratio_4s,ratio_3s,ratio_2s,ratio_1s]])
        df.to_csv("rating_ratio.csv",header=False,mode="a")

        return item