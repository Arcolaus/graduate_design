## 关于spider中，编写class时`start_request()`函数向`parse()`函数传递数据
scrapy在start_requests中发出请求时，需要传入一些参数进行动态控制。由于scrapy默认并发数是16，为保证scrapy的请求的并发性，将其改为串行执行显然严重影响效率，因此不考虑采用全局变量的方法。因此需要使用`callback`函数进行信息的传递

## 豆瓣短评页
豆瓣每部电影的[短评页](https://movie.douban.com/subject/1291546/comments?start=0&limit=121&status=P&sort=new_score)至多只有121条短评，即url参数 `limit` 最大为120，根据以爬取的数据来看top250中电影短评数最少有30000条左右。由于豆瓣网本身设计，每页默认短评数为20，虽然提高`limit`对应值可以提高爬取速度，但是会出现网页不存在等bug，故仍采用默认每页短评数量，出于反爬机制或者网页本身bug，参数最大为`start=580&limit=20`

## 并发数的设置
并发数不要超过8，可有效避免验证码问题