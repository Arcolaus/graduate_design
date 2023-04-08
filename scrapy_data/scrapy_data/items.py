# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Movie(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	movie_name=scrapy.Field()
	movie_url=scrapy.Field()


class MovieDetail(scrapy.Item):
	movie_title = scrapy.Field()        # 片名
	movie_detail_url=scrapy.Field()     # 详情页url
	movie_id=scrapy.Field()             # 豆瓣电影唯一标识id
	movie_final_score=scrapy.Field()    # 得分
	movie_score_num=scrapy.Field()    	# 评分人数
	movie_comment_num=scrapy.Field()	# 短评数

class MovieComment(scrapy.Item):		
	comment_score=scrapy.Field()		# 给出的打分
	comment_stars=scrapy.Field()		# 获得的“有用”
	comment_movie_id=scrapy.Field()		# 对应的电影id
	comment_content=scrapy.Field()		# 短评内容（需要清洗，去除各种转义符
