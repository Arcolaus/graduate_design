import scrapy


class HttpproxyipSpider(scrapy.Spider):
    name = "httpProxyIp"
    allowed_domains = ["icanhazip.com"]
    start_urls = ["http://myip.ipip.net"]

    custom_settings={
		'ITEM_PIPELINES': {
            },
        "DOWNLOADER_MIDDLEWARES":{
            "scrapy_data.middlewares.ScrapyDataDownloaderMiddleware": 300,
        }
	}

    def parse(self, response):
        print('IP info :', response.text)
        # print(response.status)
