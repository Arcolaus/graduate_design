import scrapy
import pandas as pd
from scrapy import Selector, Request

from scrapy_data.items import MovieDetail


class ProcessUrlDetailSpider(scrapy.Spider):
	name = "process_url_detail"
	allowed_domains = ["movie.douban.com"]
	# start_urls = ["https://movie.douban.com/subject/1292213/"]

	def start_requests(self):
		self.movie_list=pd.read_csv(r'F:\graduate_design\scrapy_data\output.csv',encoding='gbk')

		for page in self.movie_list.itertuples():

			# self.movie_title=getattr(page,'title')
			# self.movie_url=getattr(page,"url")
			# 以上获取单个item信息的方法只有在并发数为1的时候才可行
			# 原因是，目测scrapy的大致工作原理中，start_request()函数和parse()函数是异步的
			# 所以定义在类内的变量无法准确用于parse()函数的调用

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
