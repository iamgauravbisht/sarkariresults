import scrapy
from sarkariresult.items import HeadlineItem


class HeadlineSpider(scrapy.Spider):
    name = "headline"
    allowed_domains = ["www.sarkariresult.com"]
    start_urls = ["https://www.sarkariresult.com/"]

    def parse(self, response):
        headline = HeadlineItem()
        for i in range(1, 9):
            headline['headlineText'] = response.css(f"div#image{i} a::text").get()
            headline["headlineLink"]= response.css(f"div#image{i} a").attrib["href"]

            yield headline
        pass
