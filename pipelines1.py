# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from .models import *
import logging as l
from datetime import datetime as dt

class EcommercePipeline:
    def process_item(self, item, spider):
        return item

class SosDumpPipeline:
    def process_item(self, item, spider):
        SOS(
            timestamp = item['timestamp'],
            website = item['website'],
            segment = item['segment'],
            total_count = item['total_count'],
            brand = item['brand'],
            item_category = item['item_category'],
            count = item['count'],
            processor = item['processor'],
        ).save()
        return item
        
class CategorySearchDumpPipeline:
    def process_item(self, item, spider):
        Category(
            timestamp = item['timestamp'],
            website = item['website'],
            ratings = item['ratings'],
            processor_type = item['processor_type'],
            offer = item['offer'],
            processor_model = item['processor_model'],
            price = item['price'],
            page_count = item['page_count'],
            reviews = item['reviews'],
            gpu_type = item['gpu_type'],
            link = item['link'],
            item_id = item['item_id'],
            gpu = item['gpu'],
            order = item['order'],
            image_count = item['image_count'],
            product_name = item['product_name'],
            processor = item['processor'],
            page = item['page'],
            brand_name = item['brand_name'],
            item_category = item['item_category'],
            segment = item.get('segment',None)
        ).save()
        Search(
            timestamp = item['timestamp'],
            website = item['website'],
            ratings = item['ratings'],
            processor_type = item['processor_type'],
            offer = item['offer'],
            processor_model = item['processor_model'],
            price = item['price'],
            page_count = item['page_count'],
            reviews = item['reviews'],
            gpu_type = item['gpu_type'],
            link = item['link'],
            item_id = item['item_id'],
            gpu = item['gpu'],
            order = item['order'],
            image_count = item['image_count'],
            product_name = item['product_name'],
            processor = item['processor'],
            page = item['page'],
            brand_name = item['brand_name'],
            item_category = item['item_category'],
            segment = item.get('segment',None)
        ).save()
        return item
       
class AmazonProductAnalyzerDumpPipeline:
    def process_item(self, item, spider):
        AmazonProductAnalyzer(
            product_url = item['product_url'],
            product_name = item['product_name'],
            product_asin = item['product_asin'],
            timestamp = item['timestamp'],
            symbols_and_emojis_not_in_title = item['symbols_and_emojis_not_in_title'],
            title_length = item['title_length'],
            bullet_count = item['bullet_count'],
            bullet_points_length = item['bullet_points_length'],
            bullet_first_letter_capital = item['bullet_first_letter_capital'],
            bullet_not_all_caps = item['bullet_not_all_caps'],
            description_length = item['description_length'],
            main_image_url = item['main_image_url'],
            main_image_size = item['main_image_size'],
            main_image_background_white = item['main_image_background_white'],
            image_count = item['image_count'],
            includes_video = item['includes_video'],
            reviews = item['reviews'],
            ratings = item['ratings']
        ).save()
        return item

class ConsumerComplianceDumpPipeline:
    def process_item(self, item, spider):
        ConsumerCompliance(
            link = item['link'],
            product_name = item['product_name'],
            item_category = item['item_category'],
            brand_name = item['brand_name'],
            processor_type = item['processor_type'],
            processor_model = item['processor_model'],
            ratings = item['ratings'],
            item_id = item['item_id'],
            product_text = item['product_text'],
            hero_text = item['hero_text'],
            other_text = item['other_text'],
            cpu_logo = item['cpu_logo'],
            gpu_logo = item['gpu_logo'],
            segment1 = item['segment1'],
            segment2 = item['segment2'],
            website = item['website'],
            complete = item['complete'],
            logo_matched = item['logo_matched'],
            review_scraped = item.get('review_scraped',False)
        ).save()
        return item

class ConsumerMessagingDumpPipeline:
    def process_item(self, item, spider):
        ConsumerMessaging(
            website = item['website'],
            index = item['index'],
            item_category = item['item_category'],
            item_id = item['item_id'],
            message = item['message'],
            heading = item['heading']
        ).save()
        return item
# class EcommercePipeline(object):
#     def init(self):
#         pass

#     def open_spider(self, spider):
#         sov_file = open('dell_jp_desk_02_20.csv','w')
#         self.sov_writer = csv.writer(sov_file)
#         self.sov_writer.writerow(["brand","processor","segment","count","total_count","result_type","timestamp","website","item_category"])
#         details_file = open('dell_jp_desk_details_feed_02_20.csv','w')
#         self.details_writer = csv.writer(details_file)
#         self.details_writer.writerow(["item_id","processor_type","processor_model","link","product_name","location","result_type","timestamp","website","item_category"])

#     def process_item(self, item, spider):
#         if item['result_type'] == 'details':
#             self.details_writer.writerow([item["item_id"],item["processor_type"],item["processor_model"],item["link"],item["product_name"],item["location"],item["result_type"],item["timestamp"],item["website"],item["item_category"]])
#         elif item['result_type'] == 'sov':
#             self.sov_writer.writerow([item["brand"],item["processor"],item["segment"],item["count"],item["total_count"],item["result_type"],item["timestamp"],item["website"],item["item_category"]])
#         return item