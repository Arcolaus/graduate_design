import scrapy


class HttpproxyipSpider(scrapy.Spider):
    name = "httpProxyIp"
    allowed_domains = ["icanhazip.com"]
    start_urls = ["http://myip.ipip.net"]

    def parse(self, response):
        print('代理后的ip: ', response.text)
