import scrapy

from scrapy import Request,Selector

from scrapy_data.items import Movie

class GetMovieListSpider(scrapy.Spider):
    name = "get_movie_list"
    allowed_domains = ["movie.douban.com","douban.com"]
    # start_urls = ["http://movie.douban.com/"]

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_data.pipelines.ExportMovieList': 200,},
    }

    def start_requests(self):
        for page in range(1):
            yield Request(
                url=f'https://movie.douban.com/top250?start={page * 25}&filter='
            )
    def parse(self,response,**kwargs):
        sel=Selector(response)
    
        list_items = sel.css('#content > div > div.article > ol > li')

        for item in list_items:

            movie_item=Movie()
            movie_item['title'] = item.css("span.title::text").extract_first()
            movie_item['url'] = item.css("div.hd > a::attr(href)").extract_first()
            movie_item['id']=movie_item['url'].split('/')[-2]

            yield movie_item