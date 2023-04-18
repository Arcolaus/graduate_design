import scrapy
import pandas as pd
from scrapy import Selector, Request

from scrapy_data.items import MLWorkDetail

class MlWorkDetailSpider(scrapy.Spider):
	name = "ml_work_detail"
	allowed_domains = ["movie.douban.com"]
	# start_urls = ["https://movie.douban.com/subject/6722879/","https://movie.douban.com/subject/30403219/"]

	custom_settings={
		'ITEM_PIPELINES': {'scrapy_data.pipelines.ExportMLWorkDetail': 300,},
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

	def parse(self, response,**kwargs):
		sel=Selector(response)

		work=MLWorkDetail()
		
		work["title"]=response.meta["title"]
		work["work_id"]=response.url.split("/")[-2]

		collect=sel.css("#subject-others-interests > div > a")
		watched_num=0

		if len(collect) == 2:
			watched_num=sel.css("#subject-others-interests > div > a:nth-child(1)::text").extract_first()
		elif len(collect) == 3:
			watched_num=sel.css("#subject-others-interests > div > a:nth-child(2)::text").extract_first()

		work["watched_num"]=int(str(watched_num)[:-3])
		work["score_num"]=sel.css('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span::text').extract_first()

		work["comment_num"]=sel.css('#comments-section > div.mod-hd > h2 > span > a::text').extract_first()
		
		yield work
