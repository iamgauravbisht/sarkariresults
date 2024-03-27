import scrapy

class PageSpider(scrapy.Spider):
    name = "pages"
    allowed_domains = ["www.sarkariresult.com"]
    start_urls = ["https://www.sarkariresult.com/upsssc/23exam2016/"]

    def parse(self, response):
        name_of_post = response.xpath('/html/body/div[1]/div[1]/tr[2]/td[2]/text()').get()
        date = response.xpath('/html/body/div[1]/div[1]/tr[3]/td[2]/text()').get()
        info = response.xpath('/html/body/div[1]/div[1]/tr[4]/td[2]/text()').get()
        headingOne = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[1]/td/h2[1]/span/b/text()').get()
        headingTwo = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[1]/td/h2[2]/span/b/text()').get()
        headingThree = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[1]/td/h2[3]/span/b/text()').get()
        heading = f"{headingOne}\n{headingTwo}\n{headingThree}"
        
        importantDatesTitle = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[2]/td[1]/h2/span/b/text()').get()
        importantDatesData = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[2]/td[1]//ul/li')

        ApplicationFeeTitle = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[2]/td[2]/h2/span/b/text()').get()
        ApplicationFeeData = response.xpath('/html/body/div[1]/div[1]/table/tbody/tr[2]/td[2]/ul/li')

        important_date_list = [('title',importantDatesTitle)]
        application_fee_list = [('title',ApplicationFeeTitle)]
        tableRow=[]
        tableDetails=response.xpath('/html/body/div[1]/div[1]/table/tbody/tr')
        for index, tr_element in enumerate(tableDetails):
            if(index==0 or index==1):
                continue
            else:
                # print("Index:", index)
                tr_html = tr_element.extract()
                tr_html_lower = tr_html.lower()
                # print("tr_html_lower",tr_html_lower)
                contains_sarkariresult = 'sarkariresult' in tr_html_lower or 'sarkariresults' in tr_html_lower
                # print("Contains 'sarkariresult':", contains_sarkariresult)
                # now put all this data into the table and just print this into the page 
                if not contains_sarkariresult:
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

        # Print the list containing key-value pairs
        self.logger.info("Key-Value Pairs:")
        self.logger.info(important_date_list)
        self.logger.info("Application Fee:")
        self.logger.info(application_fee_list)
        

        # You can yield the data or process it further
        yield {
            "name_of_post": name_of_post,
            "date": date,
            "info": info,
            "heading": heading,
            "important_dates": important_date_list,
            "application_fee_data": application_fee_list,
            "table Rows": tableRow
        }


# i want this page to fetch top 50 post data and then compare it with the every box and then if any thing is changed or updated update the whole pages data