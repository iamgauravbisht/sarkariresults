import scrapy


class HomepageSpider(scrapy.Spider):
    name = "homepage"
    allowed_domains = ["www.sarkariresult.com"]
    start_urls = ["https://www.sarkariresult.com"]

    def parse(self, response):
        boxs=response.css("div#box1 , div#box2")
        for box in boxs:
            box_title = box.css("div#heading div a::text").get()
            box_link = box.css("div#heading div a").attrib["href"]

            # if (box_link=='https://www.sarkariresult.com/answerkey/'):
            #     yield response.follow(box_link,callback=self.answerkeyParser)

            # Result, Certificate Verification, Admit Card, Syllabus, Important, Latest Jobs, Admission
            if box_title=="Admission":
                yield scrapy.Request(
                box_link,
                callback=self.parse_box_listed_data,
                meta={"boxTitle": box_title,"boxLink":box_link},
            )

        # headlines = []
        # for i in range(1, 9):
        #     headlines.append(
        #         {
        #             "headline": response.css(f"div#image{i} a::text").get(),
        #             "headlineLink": response.css(f"div#image{i} a").attrib["href"],
        #         }
        #     )

        # for i in range(len(headlines)):
        #     yield headlines[i]
        pass

    def parse_box_listed_data(self, response):
        box_title = response.meta["boxTitle"]
        box_link = response.meta['boxLink']
        listings = response.css('div#post ul li')

        for listing in listings:
            post_text = listing.css('a::text').get()
            post_link = listing.css('a::attr(href)').get()
            yield{
                'boxLink':box_link,
                'boxTitle':box_title,
                'postText':post_text,
                'postLink':post_link
            }
            
    
    def answerkeyParser(self,response):
        listings = response.css('div#post ul')
        for listing in listings:
            post_text = listing.css('a::text').get()
            post_link = listing.css('a::attr(href)').get()
           
            yield{
                'boxLink':'https://www.sarkariresult.com/answerkey/',
                'boxTitle':'Answer Key',
                'postText':post_text,
                'postLink':post_link
                }
    
            
            
          
# boxHeading,boxLink
# Result,https://www.sarkariresult.com/result/
# Answer Key,https://www.sarkariresult.com/answerkey/
# Certificate Verification,https://www.sarkariresult.com/verification/
# Admit Card,https://www.sarkariresult.com/admitcard/
# Syllabus,https://www.sarkariresult.com/syllabus/
# Important,https://www.sarkariresult.com/important/
# Latest Jobs,https://www.sarkariresult.com/latestjob/
# Admission,https://www.sarkariresult.com/admission/


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


# <ul>
#   <li>
#       <a href="https://www.sarkariresult.com/bank/sbi-po-sep2023/" target="_blank">
#           SBI PO 2023 Final Result 
#       </a>  
#   </li>
# </ul>