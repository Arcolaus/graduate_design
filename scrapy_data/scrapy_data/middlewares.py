# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import requests

import pandas as pd
from scrapy import signals
from fake_useragent import UserAgent
from twisted.internet.error import TimeoutError,ConnectError,TCPTimedOutError


secret_id="oxxj0f0lr88v4ufcxbts"
secret_key="jye818mqd8jue46cz2gpeehjdmom8mq3"
signature="o0eiedvjs7ghnra26v6lxvmcb0"

# useful for handling different item types with a single interface
def get_cookies_dict():
    cookies_str='ll="118324"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.15728; _ga=GA1.2.1758259612.1673093337; gr_user_id=c22f60b8-976c-4e50-ba77-1927a203660f; bid=sXRWT7Wcd_Q; __utmz=30149280.1680787849.59.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ct=y; dbcl2="157285472:gmxq8naf6Gs"; ck=hTYR; __utmc=30149280; _pk_ref.100001.8cb4=["","",1681270786,"https://movie.douban.com/subject/27010768/comments?status=P"]; _pk_id.100001.8cb4=278c63ff85fc6183.1675531249.; frodotk_db="f0f0ce00272e53b8d2d26a00758afb28"; ap_v=0,6.0; __utma=30149280.1758259612.1673093337.1681292379.1681307192.80; __utmb=30149280.0.10.1681307192'
    cookies_dict={}
    
    for item in cookies_str.split('; '):
        key,value=item.split('=',maxsplit=1)
        cookies_dict[key]=value
    
    return cookies_dict

COOKIES_DICT = get_cookies_dict()

PROXY_API="http://j879.kdltps.com:15818"

class ScrapyDataSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)



class ScrapyDataDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    kdl_proxy=('j879.kdlapi.com', '15818')

    def __init__(self) -> None:
        self.max_failed = 3
        self.faild_times = 0

        pass

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        request.cookies=COOKIES_DICT

        ua=UserAgent()
        request.meta["User-Agent"]=ua

        # request.meta["proxy"] = self.get_proxy("API")
        # if not request.meta.get("proxy"):
            # request.meta["proxy"] = self.get_proxy("API")
        
        return None

    def process_response(self, request, response, spider):

        # if response.status != 200:
        #     print("response status error")
        #     self.faild_times += 1

        # if self.faild_times >= self.max_failed:
        #     self.change_proxyIP()
        #     print("Proxy IP changed")
        #     self.faild_times = 0
        #     del request.meta['proxy']
        #     return request
        
        return response

    def process_exception(self, request, exception, spider):

        del request.meta['proxy']
        return request
 

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def get_proxy(self,option):
        if option == "API":
            api="http://%(proxy)s/" % {"proxy": "j879.kdltps.com:15818"}
            return api
        
        if option == "LOCAL":
            df=pd.read_csv("proxy_list.csv")
            cur_proxy = random.choice(df["proxy_url"])
            return cur_proxy
        
    def change_proxyIP(self):
        url="https://tps.kdlapi.com/api/changetpsip?secret_id={}}&signature={}".format(secret_id,signature)
        print(requests.get(url).text)
        