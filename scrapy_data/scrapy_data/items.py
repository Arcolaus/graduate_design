# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Movie(scrapy.Item):
	title=scrapy.Field()
	url=scrapy.Field()
	id=scrapy.Field()

class MovieDetail(scrapy.Item):
	title = scrapy.Field()			# 片名
	url=scrapy.Field()				# 详情页url
	id=scrapy.Field()             	# 豆瓣电影唯一标识id
	rating=scrapy.Field()    		# 得分
	score_num=scrapy.Field()    	# 评分人数
	comment_num=scrapy.Field()		# 短评数

class MovieComment(scrapy.Item):
	movie_title=scrapy.Field()	# 短评对应的片名		
	movie_id=scrapy.Field()		# 对应的电影id
	score=scrapy.Field()		# 给出的打分
	stars=scrapy.Field()		# 获得的“有用”
	content=scrapy.Field()		# 短评内容（需要清洗，去除各种转义符）

class ProxyIP(scrapy.Item):
	ip=scrapy.Field()
	port=scrapy.Field()
	proxy_url=scrapy.Field()

class Celebrity(scrapy.Item):
	name=scrapy.Field()
	cel_id=scrapy.Field()
	works_page_url=scrapy.Field()

class MLWorkDetail(scrapy.Item):
	title=scrapy.Field()
	work_id=scrapy.Field()
	score_num=scrapy.Field()
	watched_num=scrapy.Field()
	comment_num=scrapy.Field()

class WorkRatio(scrapy.Item):
	title=scrapy.Field()
	work_id=scrapy.Field()
	score_num=scrapy.Field()
	ratio_5s=scrapy.Field()
	ratio_4s=scrapy.Field()
	ratio_3s=scrapy.Field()
	ratio_2s=scrapy.Field()
	ratio_1s=scrapy.Field()
