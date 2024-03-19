import scrapy


class HomepageSpider(scrapy.Spider):
    name = "homepage"
    allowed_domains = ["www.sarkariresult.com"]
    start_urls = ["https://www.sarkariresult.com"]

    def parse(self, response):
        box1 = response.css("div#box1")
        box2 = response.css("div#box2")
        boxs = box1 + box2
        for box in boxs:
            yield {
                "boxHeading": box.css("div#heading div a::text").get(),
                "boxLink": box.css("div#heading div a").attrib["href"],
            }
        headlines = []
        for i in range(1, 9):
            headlines.append(
                {
                    "headline": response.css(f"div#image{i} a::text").get(),
                    "headlineLink": response.css(f"div#image{i} a").attrib["href"],
                }
            )

        for i in range(len(headlines)):
            yield headlines[i]

        pass



# how to get box name and the heading and post
# select them using div div#heading and div div#post selectors
# inside div#heading there are two divs with one with headingname (anchor tag)
# <div id="heading">
# <div align="center">
# <a href="https://www.sarkariresult.com/admitcard/" target="_blank">Admit Card</a>
# </div>
# <div style="margin-top:1380px">
# <div id="view" align="center"><a href="https://www.sarkariresult.com/admitcard/" target="_blank">View More</a></div>
# </div>
# </div>

# inside div#post ul li there are list of posts with anchor tag and text

# getting top 8 headings
# <div id="image1" align="center">
# <a href="https://www.sarkariresult.com/railway/rrb-technician-02-2024/">RRB Technician<br>Apply Online</a>
# </div>
