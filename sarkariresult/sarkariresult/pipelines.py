# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# from scrapy.exceptions import DropItem
from sarkariresult.items import BoxItem
from sarkariresult.items import pageItem
from pymongo.mongo_client import MongoClient

class BoxItemPipeline:
    def process_item(self, item, spider):

        


        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        # print("items in pipeline", item)

        # self.logger.info(" items  :")
        # self.logger.info(item)
        for field_name in field_names:
            if field_name == 'boxTitle' or field_name == 'boxLink' or field_name == 'postLink' or field_name == 'postText':
                print("i am inside box_items")
            if field_name == 'name_of_post':
                print("i am inside page_items ggfdksgjfgsjfdsjgfkjjhgasfjgsfjkgfdsjhgdfsjg")


        return item



#     name_of_post=scrapy.Field()
#     date=scrapy.Field()
#     info=scrapy.Field()
#     heading=scrapy.Field()
#     important_date_list=scrapy.Field()
#     application_fee_list=scrapy.Field()
#     tableRow=scrapy.Field()