import scrapy


class GetmovielistSpider(scrapy.Spider):
    name = "getMovieList"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["http://movie.douban.com/"]

    def parse(self, response):
        pass
