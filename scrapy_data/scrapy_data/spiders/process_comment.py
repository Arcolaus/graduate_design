import scrapy
import pandas as pd

from scrapy import Selector,Request

from scrapy_data.items import MovieComment

class ProcessCommentSpider(scrapy.Spider):
    name = "process_comment"
    allowed_domains = ["movie.douban.com"]
    # start_urls = ["https://movie.douban.com/subject/27010768/comments?start=0&limit=20&status=P"]

    custom_settings={
		'ITEM_PIPELINES': {
            "scrapy_data.pipelines.ExportComments": None,        # 导出top250的所有短评
            "scrapy_data.pipelines.ExportCeleComments": 500,    # 导出对照组所有短评
        },
        "DOWNLOADER_MIDDLEWARES":{
            "scrapy_data.middlewares.ScrapyDataDownloaderMiddleware": 300,
        },
	}

    def start_requests(self):
        # fl=pd.read_csv("movie_list.csv") # 爬取top250的短评
        fl=pd.read_csv("cele_works.csv") # 爬取对照组短评

        for page in fl.itertuples():
            movie_url=getattr(page,"url")
            movie_title=getattr(page,"title")
            movie_id=getattr(page,"id")
            
            for it in range(0,28):
                yield Request(url=(movie_url+f"comments?start={it * 20}&limit=20&status=P"),
                              meta={
                                "title":movie_title,
                                "id":movie_id
                              },
                              callback=self.parse)


    def parse(self, response):
        sel=Selector(response)

        comment_items=sel.css("#comments >  div.comment-item")

        for item in comment_items:
            comment=MovieComment()

            comment["movie_title"]=response.meta["title"]
            comment["movie_id"]=response.meta["id"]

            comment["score"]=item.css("div.comment >h3>span.comment-info>span:nth-child(3)::attr(class)").extract_first()

            comment["stars"]=item.css("div.comment >h3>span.comment-vote>span::text").extract_first()
            content_t= item.css("div.comment > p > span::text").extract_first()

            content_t=str(content_t).replace("\t","")
            content_t=content_t.replace("\r","")
            comment["content"] = content_t.replace("\n","")

            yield comment