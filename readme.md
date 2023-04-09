## 关于spider中，编写class时`start_request()`函数向`parse()`函数传递数据
scrapy在start_requests中发出请求时，需要传入一些参数进行动态控制。由于scrapy默认并发数是16，为保证scrapy的请求的并发性，将其改为串行执行显然严重影响效率，因此不考虑采用全局变量的方法。因此需要使用`callback`函数进行信息的传递