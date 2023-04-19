import scrapy
import scrapy
import pandas as pd
from scrapy import Selector, Request

from scrapy_data.items import WorkRatio


class RatingRatioSpider(scrapy.Spider):
	name = "rating_ratio"
	allowed_domains = ["movie.douban.com"]
	# start_urls = ["http://movie.douban.com/"]

	custom_settings={
		'ITEM_PIPELINES': {'scrapy_data.pipelines.ExportRatingRatio': 300,},
	}

	def start_requests(self):
		self.work_list=pd.read_csv("ml_work_list.csv")

		for page in self.work_list.itertuples():
			yield Request(
				url=getattr(page,"url"),
				meta={
						"title":getattr(page,'title'),
					},
				callback=self.parse
			)
	# https://movie.douban.com/subject/1292720/
	def parse(self, response,**kwargs):
		sel=Selector(response)

		work=WorkRatio()

		work["title"]=response.meta["title"]
		work["work_id"]=response.url.split("/")[-2]
		work["score_num"]=sel.css("#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span::text").extract_first()

		work["ratio_5s"]=sel.css("div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(1) > span.rating_per::text").extract_first()
		work["ratio_4s"]=sel.css("div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(2) > span.rating_per::text").extract_first()
		work["ratio_3s"]=sel.css("div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(3) > span.rating_per::text").extract_first()
		work["ratio_2s"]=sel.css("div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(4) > span.rating_per::text").extract_first()
		work["ratio_1s"]=sel.css("div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(5) > span.rating_per::text").extract_first()
		
		yield work
