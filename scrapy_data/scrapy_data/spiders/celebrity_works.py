import scrapy
import pandas as pd


from scrapy_data.items import Movie
from scrapy import Request,Selector

class CelebrityWorksSpider(scrapy.Spider):
    name = "celebrity_works"
    allowed_domains = ["movie.douban.com"]
    # start_urls = ["http://movie.douban.com/"]

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_data.pipelines.ExportCeleWorksList': 200,},
    }

    def start_requests(self):
        
        df=pd.read_csv("celebrities_list.csv")

        for page in df["url"]:
            for count in range(2):
                yield Request(
                    url=str(page)+"movies?start={}&format=text&sortby=time&role=A1".format(count)
                )

    def parse(self, response, **kwargs):
        sel=Selector(response)

        list_items=sel.css("#content > div > div.article > div.list_view > table > tbody > tr")

        for item in list_items:

            onScreen=item.css("tr > td[headers=m_name] > strong::text").extract_first()
            rated=item.css("td[headers=mc_rating] > div > span.rating_nums::text").extract_first()
            

            movie_item=Movie()
            movie_item["title"]=item.css("td[headers=m_name] > a::text").extract_first()
            movie_item["url"]=item.css("td[headers=m_name] > a::attr(href)").extract_first()
            movie_item["id"]=movie_item['url'].split('/')[-2]

            if onScreen =="（未上映）" or rated == None:
                continue
            print(movie_item["title"],rated)

            yield movie_item
