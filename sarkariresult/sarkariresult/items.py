# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BoxItem(scrapy.Item):
    boxTitle=scrapy.Field()
    boxLink=scrapy.Field()
    postText=scrapy.Field()
    postLink=scrapy.Field()
    pass

class HeadlineItem(scrapy.Item):
    headlineText=scrapy.Field()
    headlineLink=scrapy.Field()
    pass

class pageItem(scrapy.Item):
    name_of_post=scrapy.Field()
    date=scrapy.Field()
    info=scrapy.Field()
    heading=scrapy.Field()
    important_date_list=scrapy.Field()
    application_fee_list=scrapy.Field()
    tableRow=scrapy.Field()
    post_id=scrapy.Field()


