import scrapy

from scrapy import Request,Selector

from scrapy_data.items import ProxyIP

class CollectProxySpider(scrapy.Spider):
    name = "collect_proxy"
    allowed_domains = ["kuaidaili.com"]
    # start_urls = ["http://kuaidaili.com/"]

    custom_settings={
		'ITEM_PIPELINES': {
            'scrapy_data.pipelines.ExportProxy': 300,
        },
        "DOWNLOADER_MIDDLEWARES":{
        },
        "USER_AGENT":{
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
        },
	}

    def start_requests(self):
        for page in range(2,4):
            yield Request(url=f"https://www.kuaidaili.com/free/inha/{page}/")

    def parse(self, response):
        sel=Selector(response)

        list_items = sel.css("#list > table > tbody > tr")

        for item in list_items:
            proxy=ProxyIP()
            proxy["ip"]=item.css("td[data-title=IP]::text").extract_first()
            proxy["port"]=item.css("td[data-title=PORT]::text").extract_first()
            proxy["proxy_url"]="http://"+str(proxy["ip"])+":"+str(proxy["port"])

            yield proxy
