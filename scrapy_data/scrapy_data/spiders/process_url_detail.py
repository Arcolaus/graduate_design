import scrapy
import pandas as pd
from scrapy import Selector, Request

from scrapy_data.items import MovieDetail


class ProcessUrlDetailSpider(scrapy.Spider):
	name = "process_url_detail"
	allowed_domains = ["movie.douban.com"]
	# start_urls = ["https://movie.douban.com/subject/1292213/"]

	custom_settings={
		'ITEM_PIPELINES': {'scrapy_data.pipelines.ExportMovieDetail': 300,},
	}

	def start_requests(self):
		self.movie_list=pd.read_csv('movie_list.csv') # top250

		for page in self.movie_list.itertuples():

			yield Request(
				url=getattr(page,"url"),
				meta={
						"title":getattr(page,'title'),
					},
				callback=self.parse
			)

	def parse(self, response,**kwargs):
		sel=Selector(response)

		detail_movie=MovieDetail()

		detail_movie['title']=response.meta["title"]
		detail_movie['url']=response.url
		detail_movie['id']=response.url.split("/")[-2]

		detail_movie["rating"]=sel.css("#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong::text").extract_first()
		detail_movie["score_num"]=sel.css('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span::text').extract_first()
		detail_movie["comment_num"]=sel.css('#comments-section > div.mod-hd > h2 > span > a::text').extract_first()

		yield detail_movie
