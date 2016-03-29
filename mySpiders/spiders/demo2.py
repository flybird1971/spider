# from scrapy.spider import BaseSpider

# class Demo2Spider(BaseSpider):
#     name = "demo2"
#     allowed_domains = ["dmoz.org"]
#     start_urls = [
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
#     ]

#     def parse(self, response):
#         filename = response.url.split("/")[-2] + '.html'
#         open(filename, 'wb').write(response.body)