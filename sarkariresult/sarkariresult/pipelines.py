# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient
from datetime import datetime

class BoxItemPipeline:

    index = {
        'result': 1,
        'syllabus': 1,
        'admitcard': 1,
        'answerkey': 1,
        'certificateverification': 1,
        'important': 1,
        'latestjobs': 1,
        'admission': 1
    }
        
    def process_item(self, item, spider):
        client = MongoClient('mongodb+srv://govjobaspirants:GM24FjGwvBWbF6Jg@cluster0.iaapyui.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        db = client['govjobaspirants']

        adapter = ItemAdapter(item)
        field_names = adapter.field_names()



        for field_name in field_names:
            if field_name == 'boxTitle':
                value = adapter.get('boxTitle');
                if value == 'Result':
                    mycol = db["result"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText'),"index": self.index['result']}
                    mycol.insert_one(mydict);
                    self.index['result']+=1;
                elif value == 'Admit Card':
                    mycol = db["admitcard"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText'),"index": self.index['admitcard']}
                    mycol.insert_one(mydict);
                    self.index['admitcard']+=1;
                elif value == 'Syllabus':
                    mycol = db["syllabus"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText'),"index": self.index['syllabus']}
                    mycol.insert_one(mydict);
                    self.index['syllabus']+=1;
                elif value == 'Answer Key':
                    mycol = db["answerkey"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText'),"index": self.index['answerkey']}
                    mycol.insert_one(mydict);
                    self.index['answerkey']+=1;
                elif value == 'Certificate Verification':
                    mycol = db["certificateverification"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText'),"index": self.index['certificateverification']}
                    mycol.insert_one(mydict);
                    self.index['certificateverification']+=1;
                elif value == 'Important':
                    mycol = db["important"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText'),"index": self.index['important']}
                    mycol.insert_one(mydict);
                    self.index['important']+=1;
                elif value == 'Latest Jobs':
                    mycol = db["latestjobs"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText'),"index": self.index['latestjobs']}
                    mycol.insert_one(mydict);
                    self.index['latestjobs']+=1;
                elif value == 'Admission':
                    mycol = db["admission"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText'),"index": self.index['admission']}
                    mycol.insert_one(mydict);
                    self.index['admission']+=1;
            
            if field_name == 'name_of_post':
                mycol = db["pages"]
                mydict = { "name_of_post": adapter.get('name_of_post'), "date": adapter.get('date'), "info": adapter.get('info'), "heading": adapter.get('heading'), "important_date_list": adapter.get('important_date_list'), "application_fee_list": adapter.get('application_fee_list'), "tableRow": adapter.get('tableRow'), "post_id": adapter.get('post_id')}
                mycol.insert_one(mydict);
        

        return item


from datetime import datetime

class updateItemPipeline:
        
    def process_item(self, item, spider):
        client = MongoClient('mongodb+srv://govjobaspirants:GM24FjGwvBWbF6Jg@cluster0.iaapyui.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        db = client['govjobaspirants']

        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        for field_name in field_names:
            if field_name == 'boxTitle':
                value = adapter.get('boxTitle');
                if value == 'Result':
                    mycol = db["result"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText'),
                    }
                    # first check if the post already exists
                    if mycol.find_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]}) is None:
                        mydict['createdat'] = datetime.now();
                        mycol.insert_one(mydict);
                    else:
                        mycol.update_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]},{"$set": mydict});

                elif value == 'Admit Card':
                    mycol = db["admitcard"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText')}
                    if mycol.find_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]}) is None:
                        mydict['createdat'] = datetime.now();
                        mycol.insert_one(mydict);
                    else:
                        mycol.update_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]},{"$set": mydict});
                elif value == 'Syllabus':
                    mycol = db["syllabus"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText')}
                    if mycol.find_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]}) is None:
                        mydict['createdat'] = datetime.now();
                        mycol.insert_one(mydict);
                    else:
                        mycol.update_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]},{"$set": mydict});
                elif value == 'Answer Key':
                    mycol = db["answerkey"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText')}
                    if mycol.find_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]}) is None:
                        mydict['createdat'] = datetime.now();
                        mycol.insert_one(mydict);
                    else:
                        mycol.update_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]},{"$set": mydict});
                elif value == 'Certificate Verification':
                    mycol = db["certificateverification"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText')}
                    if mycol.find_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]}) is None:
                        mydict['createdat'] = datetime.now();
                        mycol.insert_one(mydict);
                    else:
                        mycol.update_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]},{"$set": mydict});
                elif value == 'Important':
                    mycol = db["important"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText')}
                    if mycol.find_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]}) is None:
                        mydict['createdat'] = datetime.now();
                        mycol.insert_one(mydict);
                    else:
                        mycol.update_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]},{"$set": mydict});
                elif value == 'Latest Jobs':
                    mycol = db["latestjobs"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText')}
                    if mycol.find_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]}) is None:
                        mydict['createdat'] = datetime.now();
                        mycol.insert_one(mydict);
                    else:
                        mycol.update_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]},{"$set": mydict});
                elif value == 'Admission':
                    mycol = db["admission"]
                    mydict = { "boxTitle": adapter.get('boxTitle'), "boxLink": adapter.get('boxLink').split('https://www.sarkariresult.com/')[1], "postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1], "postText": adapter.get('postText')}
                    if mycol.find_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]}) is None:
                        mydict['createdat'] = datetime.now();
                        mycol.insert_one(mydict);
                    else:
                        mycol.update_one({"postLink": adapter.get('postLink').split('https://www.sarkariresult.com/')[1]},{"$set": mydict});
            
            if field_name == 'name_of_post':
                mycol = db["pages"]
                mydict = { "name_of_post": adapter.get('name_of_post'), "date": adapter.get('date'), "info": adapter.get('info'), "heading": adapter.get('heading'), "important_date_list": adapter.get('important_date_list'), "application_fee_list": adapter.get('application_fee_list'), "tableRow": adapter.get('tableRow'), "post_id": adapter.get('post_id')}
                mycol.insert_one(mydict);
        

        return item




#     name_of_post=scrapy.Field()
#     date=scrapy.Field()
#     info=scrapy.Field()
#     heading=scrapy.Field()
#     important_date_list=scrapy.Field()
#     application_fee_list=scrapy.Field()
#     tableRow=scrapy.Field()