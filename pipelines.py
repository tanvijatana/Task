# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .models import *
import logging as l
from datetime import datetime as dt


class CategoryDumpPipeline:
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
            segment = item.get('segment',None),
            gpu_model = item.get('gpu_model','')
        ).save()
        return item

class RawCategoryDumpPipeline:
    def process_item(self, item, spider):
        RawCategory(
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

class SearchDumpPipeline:
    def process_item(self, item, spider):
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

class SovDumpPipeline:
    def process_item(self, item, spider):
        SOV(
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
class WebsiteDataDumpPipeline:
    def process_item(self, item, spider):
        WebsiteData( 
            timestamp = item['timestamp'],
            all_count = item['all_count'],
            website = item['website'],
            non_ryzen_count =item['non_ryzen_count'],
            ryzen_count = item['ryzen_count'],
            amd_count = item['amd_count'],
            result_type = item['result_type'],
            item_category =  item['item_category'],
        ).save()
        return item

class ReviewItemsPipeline:
    def process_item(self, item, spider):
        ReviewItems(
            extract_date = item['extract_date'],
            processor_type = item['processor_type'],
            processor_model = item['processor_model'],
            product_name = item['product_name'],
            product_link = item['product_link'],
            brand_name = item['brand_name'],
            item_category = item['item_category'],
            client = 'amd',
            channel = item['channel'],
            review_count = item['review_count'],
        ).save()
        return item
class ReviewDocumentPipeline:
    def process_item(self, item, spider):
        if item.get('is_existing' , False) == False:
            ReviewDocuments(
                person_name = item['person_name'],
                person_comment = item['person_comment'],
                person_comment_raw = item['person_comment_raw'],
                review_date = item['review_date'],
                review_rating = item['review_rating'],
                is_verfied_product = item['is_verfied_product'],
                found_helpful = item['found_helpful'],
                review_link = item['review_link'],
                product_link = item['product_link'],
                review_id = item['review_id'],
                processor_type = item['processor_type'],
                processor_model = item['processor_model'],
                item_category = item['item_category'],
                person_account_details = item['person_account_details'],
                brand_name = item['brand_name'],
                channel = item['channel'],
                product_heading = item['product_heading'],
                product_name = item['product_name'],
                product_id = item['product_id'],
                extract_date = item['extract_date'],
                is_new = item['is_new'],
                client = 'amd',
                product_rating = item['product_rating']
            ).save()
            return item
        else:
            l.error("In pipeline -->> got existing")
            return item


class EcommercePipeline:
    def process_item(self, item, spider):
        return item


class AmazonIndiaCategoryPipeline:
    def process_item(self, item, spider):
        AmazonCategoryIndia(
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
            brand = item['brand_name'],
            item_category = item['item_category'],
            product_type = item['product_type'],
            is_sponsor = item['is_sponsor'],
            is_premium = item['is_premium']
        ).save()
        return item


class AmazonIndiaSearchPipeline:
    def process_item(self, item, spider):
        AmazonSearchIndia(
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
            brand = item['brand_name'],
            item_category = item['item_category'],
            product_type = item['product_type'],
            is_sponsor = item['is_sponsor'],
            is_premium = item['is_premium']
        ).save()
        return item

class SovDetailsDumpPipeline:
    def process_item(self, item, spider):
        if item['result_type'] == 'sov':
            SOV(
                timestamp = item['timestamp'],
                website = item['website'],
                segment = item['segment'],
                total_count = item['total_count'],
                brand = item['brand'],
                item_category = item['item_category'],
                count = item['count'],
                processor = item['processor'],
            ).save()
        elif item['result_type'] == 'details':
            SOVDetails(
                timestamp = item['timestamp'],
                website = item['website'],
                item_category = item['item_category'],
                location = item['location'],
                processor_model = item['processor_model'],
                processor_type = item['processor_type'],
                item_id = item['item_id'],
                link = item['link'],
                product_name = item['product_name'],
                segment = item.get('segment',None)
            ).save()
        return item

class RawSovDetailsDumpPipeline:
    def process_item(self, item, spider):
        if item['result_type'] == 'sov':
            SOV(
                timestamp = item['timestamp'],
                website = item['website'],
                segment = item['segment'],
                total_count = item['total_count'],
                brand = item['brand'],
                item_category = item['item_category'],
                count = item['count'],
                processor = item['processor'],
            ).save()
        elif item['result_type'] == 'details':
            RawSOVDetails(
                timestamp = item['timestamp'],
                website = item['website'],
                item_category = item['item_category'],
                location = item['location'],
                processor_model = item['processor_model'],
                processor_type = item['processor_type'],
                item_id = item['item_id'],
                link = item['link'],
                product_name = item['product_name'],
                segment = item.get('segment',None)
            ).save()
        return item

class CategoryMediatorPipeline:
    def process_item(self, item, spider):
        CategoryMediator(
            timestamp = item.get('timestamp'),
            website = item.get('website'),
            ratings = item.get('ratings'),
            processor_type = item.get('processor_type'),
            offer = item.get('offer'),
            processor_model = item.get('processor_model'),
            price = item.get('price'),
            page_count = item.get('page_count'),
            reviews = item.get('reviews'),
            gpu_type = item.get('gpu_type'),
            link = item.get('link'),
            item_id = item.get('item_id'),
            gpu = item.get('gpu'),
            order = item.get('order'),
            image_count = item.get('image_count'),
            product_name = item.get('product_name'),
            processor = item.get('processor'),
            page = item.get('page'),
            brand_name = item.get('brand_name'),
            item_category = item.get('item_category'),
            segment = item.get('segment',None),
            completion = item.get('completion',False),
            attempt_no =  item.get('attempt_no', "0/0"),
            
        ).save()
        return item
               
                
class ReviewDumpPipeline:
    def process_item(self, item, spider):
        ProductReviews(
            person_name = item.get('person_name'),
            person_comment_raw = item.get('person_comment_raw'),
            person_comment = '',
            review_date = item.get('review_date'),
            review_rating = item.get('review_rating'),
            product_rating = item.get('product_rating'),
            is_verfied_product = item.get('is_verfied_product'),
            found_helpful = item.get('found_helpful'),
            review_link = item.get('review_link'),
            review_id = item.get('review_id'),
            person_account_details = item.get('person_account_details'),
            brand_name = item.get('brand_name'),
            channel = item.get('channel'),
            product_heading = item.get('product_heading'),
            product_name = item.get('product_name'),
            product_id = item.get('product_id'),
            extract_date = dt.now().date().strftime("%Y-%m-%d"),
            product_link = item.get('product_link'),
            processor_type = item.get('processor_type'),
            processor_model = item.get('processor_model'),
            item_category = item.get('item_category'),
            new_review = item.get('new_review'),
            client = item.get('client','amd'),
            sponsored = item.get('sponsored',False),
            batch = item.get('batch','A')
        ).save()
        return item

class ConsumerComplianceDumpPipeline:
    def process_item(self, item, spider):
        ConsumerCompliance(
            timestamp = item['timestamp'],
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
            timestamp = item['timestamp'],
            website = item['website'],
            index = item['index'],
            item_category = item['item_category'],
            item_id = item['item_id'],
            message = item['message'],
            heading = item['heading']
        ).save()
        return item

class AllPriceDumpPipeline:
    def process_item(self, item, spider):
        AllPrice(
            website = item['website'],
            item_category = item['item_category'],
            timestamp = item['timestamp'],
            processor = item['processor'],
            price = item['price']
        ).save()
        return item


class AmazonProductAnalyzerDumpPipeline:
    def process_item(self, item, spider):
        AmazonProductAnalyzer(
            product_url = item['product_url'],
            product_name = item['product_name'],
            product_asin = item['product_asin'],
            job_id = item['job_id'],
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
            ratings = item['ratings'],
            email = item.get('email'),
            request_id = item.get('request_id')
        ).save()
        return item

class PincodeAvailabilityTrackerDumpPipeline:
    def process_item(self, item, spider):
        PincodeAvailabilityTracker(
            website = item['website'],
            timestamp = item['timestamp'],
            item_id = item['item_id'],
            product_name = item['product_name'],
            product_url = item['product_url'],
            brand_name = item['brand_name'],
            client = item['client'],
            item_category = item['item_category'],
            segment = item['segment'],
            location = item['location'],
            pincode = item['pincode'],
            availability = item['availability'],
            original_price = item['original_price'],
            discounted_price = item['discounted_price']
        ).save()
        return item

class PincodePriceTrackerDumpPipeline:
    def process_item(self, item, spider):
        PincodePriceTracker(
            platform = item['platform'],
            website = item['website'],
            timestamp = item['timestamp'],
            item_id = item['item_id'],
            product_name = item['product_name'],
            product_url = item['product_url'],
            brand_name = item['brand_name'],
            client = item['client'],
            segment = item['segment'],
            item_category = item['item_category'],
            location = item['location'],
            pincode = item['pincode'],
            availability = item['availability'],
            out_of_stocks = item['out_of_stocks'],
            original_price = item['original_price'],
            discounted_price = item['discounted_price']
        ).save()
        return item
class JDLinksForReviewsDumpPipeline:
    def process_item(self, item, spider):
        JDLinksForReviews(
            product_url = item['product_url'],     # StringField()
            item_category = item['item_category'], # StringField()
            # batch = item['batch'],                 # CharField(max_length=2)
            status = item.get('status', False),
            timestamp = item['timestamp'],         # DateTimeField(default = datetime.datetime.today)
        ).save()
        return item