import scrapy
from sarkariresult.items import BoxItem
from sarkariresult.items import pageItem

class HomepageSpider(scrapy.Spider):
    name = "homepage"
    allowed_domains = ["www.sarkariresult.com"]
    start_urls = ["https://www.sarkariresult.com"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'sarkariresult.pipelines.BoxItemPipeline': 100,
        }
    }

    def __init__(self):
        super().__init__()
        self.visited_links = set()
    
    def parse(self, response):
        boxs=response.css("div#box1 , div#box2")
        for box in boxs:
            box_title = box.css("div#heading div a::text").get()
            box_link = box.css("div#heading div a").attrib["href"]

            if (box_link=='https://www.sarkariresult.com/answerkey/'):
                yield response.follow(box_link,callback=self.answerkeyParser)
            else: 
                yield response.follow(
                box_link,
                callback=self.parse_box_listed_data,
                meta={"boxTitle": box_title,"boxLink":box_link},
                )

        # Result, Certificate Verification, Admit Card, Syllabus, Important, Latest Jobs, Admission
        pass

    def parse_box_listed_data(self, response):
        box_title = response.meta["boxTitle"]
        box_link = response.meta['boxLink']
        listings = response.css('div#post ul li')

        box_item = BoxItem()

        for listing in listings:
            post_text = listing.css('a::text').get()
            post_link = listing.css('a::attr(href)').get()
            box_item['boxLink']=box_link
            box_item['boxTitle']=box_title
            box_item['postText']=post_text
            box_item['postLink']=post_link

            if post_link not in self.visited_links:                
                self.visited_links.add(post_link)
                # print("before calling the parse_page")
                yield response.follow(post_link,callback=self.parsePage,meta={"post_link":post_link})
                # yield response.follow(post_link,callback=self.parsePage,meta={"box_item": box_item})
                # print("after calling the parse_page")
            self.logger.info("final calling the box_item")
            yield box_item    

    def answerkeyParser(self,response):
        listings = response.css('div#post ul')
        box_item = BoxItem()

        for listing in listings:
            post_text = listing.css('a::text').get()
            post_link = listing.css('a::attr(href)').get()
            box_item['boxLink']='https://www.sarkariresult.com/answerkey/'
            box_item['boxTitle']='Answer Key'
            box_item['postText']=post_text
            box_item['postLink']=post_link

            if post_link not in self.visited_links:                
                self.visited_links.add(post_link)
                # print("before calling the parse_page")
                # self.logger.info("before calling the parse_page")
                yield response.follow(post_link,callback=self.parsePage,meta={"post_link":post_link})
                # yield response.follow(post_link,callback=self.parsePage,meta={"box_item": box_item})
                # self.logger.info("after calling the parse_page")
                # print("after calling the parse_page")
            self.logger.info("final calling the box_item")
            yield box_item

    def parsePage(self,response):
        post_link = response.meta['post_link']
        page_item=pageItem()

        page_item["post_id"]=post_link.split('https://www.sarkariresult.com/')[1]
        page_item["name_of_post"] = response.xpath('/html/body/div[1]/div[1]/tr[2]/td[2]/h1/text()').get()
        page_item["date"] = response.xpath('/html/body/div[1]/div[1]/tr[3]/td[2]/text()').get()
        page_item["info"] = response.xpath('/html/body/div[1]/div[1]/tr[4]/td[2]/text()').get()
        headingOne = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[1]/td/h2[1]/span/b/text()').get()
        headingTwo = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[1]/td/h2[2]/span/b/text()').get()
        headingThree = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[1]/td/h2[3]/span/b/text()').get()
        page_item["heading"] = f"{headingOne}\n{headingTwo}\n{headingThree}"
        
        importantDatesTitle = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[2]/td[1]/h2/span/b/text()').get()
        importantDatesData = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[2]/td[1]//ul/li')

        ApplicationFeeTitle = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[2]/td[2]/h2/span/b/text()').get()
        ApplicationFeeData = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[2]/td[2]/ul/li')

        important_date_list = [('title',importantDatesTitle)]
        application_fee_list = [('title',ApplicationFeeTitle)]
        tableRow=[]

        tableDetails=response.xpath('/html/body/div[1]/div[1]/table/tbody/tr')
        for index, tr_element in enumerate(tableDetails):
            if(index==0):
                continue
            else:
                # print("Index:", index)
                tr_html = tr_element.extract()
                tr_html_lower = tr_html.lower()
                # print("tr_html_lower",tr_html_lower)
                contains_sarkariresult = 'sarkari' in tr_html_lower or 'google' in tr_html_lower or 'ads' in tr_html_lower
                if not contains_sarkariresult:
                    tableRow.append(tr_html)
                
                contains_syllabus = 'syllabus' in tr_html_lower
                if contains_syllabus:
                    tableRow.append(tr_html)

        for li in importantDatesData:   
            # Extract the text content of the li element
            li_text = li.xpath('normalize-space(.)').get()
    
            # Check if the text contains ":"
            if ":" in li_text:
                # Split the text content into key and value
                key, value = li_text.split(":", 1)
        
                # Strip whitespace from the key and value
                key = key.strip()
                value = value.strip()
    
                # Append the key-value pair to the list
                important_date_list.append((key, value))
        
        applicationFeeDetails=''
        for li in ApplicationFeeData:
            # Extract the text content of the li element
            li_text = li.xpath('normalize-space(.)').get()
            applicationFeeDetails +=li_text.strip() +" \n "
        # Append the fee information to the list
        application_fee_list.append(('text',applicationFeeDetails))

        page_item["tableRow"]=tableRow
        page_item["important_date_list"] = important_date_list
        page_item["application_fee_list"] = application_fee_list

        yield page_item 
    

            



          
# boxHeading,boxLink
# Result,https://www.sarkariresult.com/result/
# Answer Key,https://www.sarkariresult.com/answerkey/
# Certificate Verification,https://www.sarkariresult.com/verification/
# Admit Card,https://www.sarkariresult.com/admitcard/
# Syllabus,https://www.sarkariresult.com/syllabus/
# Important,https://www.sarkariresult.com/important/
# Latest Jobs,https://www.sarkariresult.com/latestjob/
# Admission,https://www.sarkariresult.com/admission/

