import scrapy
from selenium import webdriver 
from datetime import datetime as dt
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from ..models import PincodeAvailabilityTracker
import logging as l
import time
from ..commons import *
# from pyvirtualdisplay import Display
import sys
import random

# Command for execution ----> scrapy crawl amazon_pin_availability_tracker

def prred(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prgreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def pryellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prcyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prlightgray(skk): print("\033[97m {}\033[00m" .format(skk))  

firefox_options = FirefoxOptions()
path = '/home/tanvi/ecommerce/geckodriver-v0.32.2-linux32/geckodriver'

pincodes = {'Delhi': ['110006', '110048', '110027', '110005'],
            'Gurgaon': ['122018', '122104'],
            'Noida': ['201301', '201310'],
            'Kolkata': ['700040', '700016'],
            'Bangalore': ['560002', '562110', '560100', '560030'],
            'Hyderabad': ['500004', '500012', '500033'],
            'Chennai': ['600014', '600032'],
            'Mumbai': ['400049', '400018', '400020', '400029'],
            'Pune': ['411038', '411005']}

product_urls_titles = {'https://www.amazon.in/India-Gate-Basmati-Rice-Super/dp/B007GZM230/ref=sr_1_4_f3_wg?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947810&refresh=2&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-4': 'India Gate Basmati Rice Bag, Super, 5kg',
                'https://www.amazon.in/India-Gate-Basmati-Rice-Rozana/dp/B01B7AEK2A/ref=sr_1_13_f3_wg_sspa?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947810&refresh=2&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-13-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9tdGY&psc=1': 'India Gate Basmati Rice, Rozana, 5kg',
                'https://www.amazon.in/India-Gate-Basmati-Rice-Mogra/dp/B075754F8F/ref=sr_1_21_f3_wg?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947637&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-21': 'India Gate Basmati Rice Bag, Mogra, 5kg',
                'https://www.amazon.in/India-Gate-Basmati-Rice-Everyday/dp/B0BBF1FT93/ref=sr_1_8_f3_wg?almBrandId=ctnow&fpw=alm&keywords=india+gate+classic+basmati+rice&qid=1678947444&s=nowstore&sprefix=india+gate+classic%2Cnowstore%2C218&sr=1-8': 'India Gate Basmati Rice Everyday 5 kg',
                'https://www.amazon.in/India-Gate-Basmati-Daily-Premium/dp/B0BB7F6T5N/ref=sr_1_7_f3_wg?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947637&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-7': 'India Gate Basmati Rice Daily Premium 5 kg',
                'https://www.amazon.in/India-Gate-Basmati-Regular-Choice/dp/B07H2WV74G/ref=sr_1_8_f3_wg?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947927&refresh=3&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-8': 'India Gate Basmati Rice Regular Choice, 5kg',
                'https://www.amazon.in/India-Gate-Weight-Watchers-Special/dp/B08H2F7V8N/ref=sr_1_12_f3_wg?almBrandId=ctnow&crid=F966UEY8G26X&fpw=alm&keywords=india+gate+basmati+rice&qid=1678947523&s=nowstore&sprefix=india+gate+basmati+rice%2Cnowstore%2C248&sr=1-12': 'India Gate Brown Rice Weight Watchers Special,  5 Kg',
                'https://www.amazon.in/India-Gate-Basmati-Rice-Dubar/dp/B009CBIGDQ/ref=sr_1_22_f3_wg?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947637&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-22': 'India Gate Dubar 5 kg + 1 kg free',
                'https://www.amazon.in/India-Gate-Basmati-Rice-Mogra/dp/B00PCCQR4O/ref=sr_1_17_f3_wg?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947637&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-17': 'India Gate Basmati Rice Bag, Mogra, 10kg',
                'https://www.amazon.in/India-Gate-Basmati-Rice-Classic/dp/B011PQTBBG/ref=sr_1_19_f3_wg?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947637&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-19': 'India Gate Classic BSMT Rice 5 Kg',
                'https://www.amazon.in/India-Gate-Basmati-Rice-Super/dp/B079GZVZS8/ref=sr_1_30_f3_wg_sspa?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947637&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-30-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9idGY&psc=1': 'India Gate Basmati Rice Super, 1kg (with Free 500g)',
                'https://www.amazon.in/INDIA-Select-Premium-Basmati-Grains/dp/B08RQ423H9/ref=sr_1_6_f3_wg?almBrandId=ctnow&fpw=alm&keywords=india+gate+classic+basmati+rice&qid=1678947444&s=nowstore&sprefix=india+gate+classic%2Cnowstore%2C218&sr=1-6': 'INDIA GATE Select Premium Basmati Rice 5 kg Pack with 1 kg',
                'https://www.amazon.in/India-Gate-Unity-Basmati-Rozzana/dp/B08H2D4PBT/ref=sr_1_28_f3_wg?almBrandId=ctnow&crid=265TOT80E9O9Q&fpw=alm&keywords=india+gate+super+basmati+rice&qid=1678947637&s=nowstore&sprefix=india+gate+super+basmati+rice%2Cnowstore%2C214&sr=1-28': 'UNITY BASMATI RICE ROZZANA 5 KG',
                'https://www.amazon.in/Unity-Authentic-Basmati-India-Gate/dp/B096VGFHN8/ref=sr_1_11_f3_wg?almBrandId=ctnow&crid=F966UEY8G26X&fpw=alm&keywords=india+gate+basmati+rice&qid=1678947523&s=nowstore&sprefix=india+gate+basmati+rice%2Cnowstore%2C248&sr=1-11': 'Unity Super Basmati Rice, 5 Kg Pack',
                'https://www.amazon.in/Daawat-Brown-Basmati-Rice-5kg/dp/B00R1BWN1U/ref=sr_1_7_f3_wg?almBrandId=ctnow&crid=3QUFTI2B689R&fpw=alm&keywords=india+gate+weight+watchers+special+brown+rice+1+kg&qid=1678948153&refresh=5&s=nowstore&sprefix=india+gate+brown+rice+1+kg%2Cnowstore%2C207&sr=1-7': 'India Gate Brown Rice Weight Watchers Special,  1 Kg'}

class AmazonPinAvailabilityTracker(scrapy.Spider):
    name = 'amazon_pin_availability_tracker'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'ecommerce.pipelines.PincodeAvailabilityTrackerDumpPipeline': 300,
        }
    }

    def __init__(self, *args, **kwargs):
        super(AmazonPinAvailabilityTracker, self).__init__(*args, **kwargs)
        # self.disp = Display().start()
        self.today_date = dt.strftime(dt.now(), "%Y-%m-%d")
        self.website = "https://www.amazon.in"
        self.master_tracking_list = []
        useragent_list = ['Mozilla/5.0 (X11; Linux i686; rv:111.0) Gecko/20100101 Firefox/111.0',
                          'Mozilla/5.0 (X11; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0',
                          'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:111.0) Gecko/20100101 Firefox/111.0',
                          'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0',
                          'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.3; rv:111.0) Gecko/20100101 Firefox/111.0',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:111.0) Gecko/20100101 Firefox/111.0']
        
        firefox_options.add_argument("user-agent=random.choice({})".format(useragent_list))
        proxies={
        "http": "http://28b9e312964c4789b24480448c5348c1:@proxy.crawlera.com:8011/",
        "https": "http://28b9e312964c4789b24480448c5348c1:@proxy.crawlera.com:8011/",}
        firefox_options.add_argument('--proxy-server={}'.format(proxies))
        self.driver = webdriver.Firefox(options=firefox_options, executable_path=path)
        self.driver.set_page_load_timeout(100)
        PincodeAvailabilityTracker.objects(website = self.website , timestamp=self.today_date , item_category='rice').delete()

    def get_segment(self, title):
        if "Super" in title or "Classic" in title:
            segment = "Premium"
        elif "Dubar" in title or "Tibar" in title or "Select" in title or "Daily Premium" in title:
            segment = "Daily Premium"
        elif "Feast Rozzana" in title or "Rozana" in title or "Regular Choice" in title or "Everyday" in title or "ROZZANA" in title:
            segment = "Regular"
        elif "Mogra" in title or "Mini Mogra" in title or "Mini Mogra II" in title:
            segment = "Economy"
        elif "health" in title or "Weight Watchers Special" in title or "Sugar Watchers Special" in title or "Nutri-watchers" in title:
            segment = "Health"
        return segment
    
    def parse(self, response):
        try:
            for loc,pin_list in pincodes.items():
                prred(loc)
                location = loc
                for pin in pin_list:
                    pin_flag = False
                    prred(pin)
                    for url,title in product_urls_titles.items():
                        prgreen(url)
                        self.driver.get(url)
                        time.sleep(15)
                        if pin_flag == False:
                            try:
                                e1 = self.driver.find_element(by=By.XPATH, value='//div[@id="glow-ingress-block"]')
                                self.driver.execute_script("arguments[0].click();", e1)
                                time.sleep(3)
                            except:
                                self.driver.save_screenshot('amazon_pin.png')
                                with open('amazon_pin.html', 'w') as html_file:
                                    html_file.write(self.driver.page_source)
                            try:
                                self.driver.find_element(by=By.XPATH, value='//input[@id="GLUXZipUpdateInput"]').clear()
                                self.driver.find_element(by=By.XPATH, value='//input[@id="GLUXZipUpdateInput"]').send_keys(pin)
                                e2 = self.driver.find_element(by=By.XPATH, value='//span[@id="GLUXZipUpdate-announce"]')
                                self.driver.execute_script("arguments[0].click();", e2)
                                time.sleep(10)
                                pin_flag = True
                            except:
                                self.driver.save_screenshot('amazon_pin.png')
                                with open('amazon_pin.html', 'w') as html_file:
                                    html_file.write(self.driver.page_source)
                        r = scrapy.Selector(text=self.driver.page_source)
                    
                        if "Unity" in url:
                            brand_name = "unity"
                        else:
                            brand_name = "india_gate"
                        res = scrapy.Selector(text=self.driver.page_source)

                        if res.xpath('//span[@class="a-size-base a-color-secondary priceBlockStrikePriceString a-text-strike"]/span/text()'):
                            price = res.xpath('//span[@class="a-size-base a-color-secondary priceBlockStrikePriceString a-text-strike"]/span/text()').extract_first().replace('₹','')
                            discounted_price = res.xpath('//span[@class="a-size-medium a-color-price priceBlockBuyingPriceString"]/span/text()').extract_first().replace('₹','')
                        elif res.xpath('//span[@class="a-size-medium a-color-price priceBlockBuyingPriceString"]/span/text()'):
                            price = res.xpath('//span[@class="a-size-medium a-color-price priceBlockBuyingPriceString"]/span/text()').extract_first().replace('₹','')
                            discounted_price = ''
                        else:
                            price =""
                            discounted_price =""

                        avai_path1 = res.xpath('//div[@id="rightCol"]//span[@class="a-size-base-plus a-text-bold"]/text()')
                        avai_path2 = res.xpath('//span[@class="a-size-medium a-color-state"]/text()')
                        
                        if avai_path1 and avai_path1.extract_first().strip() == "Sign in to get started":
                            availability = True
                        elif avai_path2 and avai_path2.extract_first().strip() == "Sign in to get started":
                            availability = True
                        else:
                            availability = False 
                        
                        item = {"website" : self.website,
                            "timestamp" : self.today_date,
                            "item_id" : url.split('/')[-2],
                            "product_name" : title,
                            "product_url" : url,
                            "brand_name": brand_name,
                            "item_category" : "rice",
                            "segment":self.get_segment(title),
                            "client":"india_gate",
                            "location" : location,
                            "pincode" : pin,
                            "availability" : availability,
                            "price" : price,
                            "discounted_price" : discounted_price}
                        self.master_tracking_list.append(item)
                    
            for item in self.master_tracking_list:
                print(item)
                print("########################")
                yield item
            # send_mail("Amazon COMPLETED", str(len(self.master_tracking_list)), "tanvi.jatana@lyxelandflamingo.com")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            message=str(exc_type)+ str(exc_obj)+' At line no : ' +str(exc_tb.tb_lineno)
            l.error(message)
            # send_mail("Amazon ERROR", str(message), "tanvi.jatana@lyxelandflamingo.com")
        finally:
            self.driver.quit()
            # self.disp.stop()