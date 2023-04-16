import scrapy
import pandas as pd


from scrapy_data.items import Movie
from scrapy import Request,Selector

class CeleWorksSpider(scrapy.Spider):
    name = "cele_works"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["http://movie.douban.com/"]

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_data.pipelines.ExportCeleWorksList': 200,},
    }

    def start_requests(self):
        
        df=pd.read_csv("cele_list.csv")

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

            yield Request(
                url=movie_item["url"],callback=self.parse_detail,
                cb_kwargs={"item":movie_item}
            )

    def parse_detail(self,response,**kwargs):
        sel=Selector(response)
        movie_item=kwargs["item"]
        ratings=sel.css("#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span::text").extract_first()
        comments=sel.css('#comments-section > div.mod-hd > h2 > span > a::text').extract_first()

        rating_num = 0
        comment_num = 0
        if ratings:
            rating_num=int(ratings)
        if comments:
            comment_num=int(comments[2:-2])

        if rating_num <10000 or comment_num < 1000:
            print("invalid: {}".format(movie_item["title"]))
            movie_item.valid=0
            return 

        yield movie_item
