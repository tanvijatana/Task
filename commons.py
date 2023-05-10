import re
import json
import pandas as pd
from datetime import datetime
from w3lib.html import remove_tags
from typing import Any, Union, List, Dict
from email.mime.text import MIMEText
from oauth2client.file import Storage
import base64
import httplib2
from apiclient import discovery
from .models import StatusReporting, RequestInfo
import logging as l
import sys
import requests, yaml
import math


BRAND_LIST  = ['acer', 'alienware', 'allied gaming', 'apple', 'asus', 'avgpc', 'avita', 'baiwei', 'beelink', 'corsair', 'craving savings', 'cyberpowerpc', 'dell', 'evoo', 'gateway', 'ibuypower', 'lenovo', 'lenovo united states inc', 'lianth', 'microsoft', 'minisforum', 'msi', 'oemgenuine', 'onn.', 'samsung', 'skytech gaming', 'thermaltake', 'lg', 'hp']

def get_processor_variants() -> list:
    """
    Description:
        - list of all processor variants
        - add if not available

    Returns:
        list: [ list of variants ]
    """
    lst = ['10900kf', '13700kf', '1135g4', '1220p', '7950x', '5300ge', '5600ge', '5650g', 'r1606g', '5400u', '4600ge', '4300ge', '4700s', '5800hs', '3015ce', '5980hx', '4500m', '5350m', '2500u', '5625u', '5650ge', '9225', '3580u', '12700kf', 'j4125', '12700f', '12800h', '1270p', '5700', '5700x', '6700', '10100f', '5250u', '5125c', '5500', '12700t', '12100f', '12400t', '1255u', '12650h', '12900hk', '12900hx', '12800hx', '6900hs', '1215u', '1235u', '4205u', 'g6405', '5405u', '8565u', '1260p', '1005g1', '12100', '12400', '12500h', '12500u', '11950h', '10100', '10100t', '10105f', '10105', '10110u', '10210u', '10200h', '12500', '12500t', '10300h', '10300', '1035g1', '1035g7', '10505', '10400', '1035g4', '10400f', '10400t', '10500', '10500t', '11600k', '12400f', 'n5095', '12600', '12900k', '12900kf', '12600k', '11400', '11600kf', '12900h', '10510u', '10810u', '10600kf', '1140g7', '11300h', '8635u', '10610u', '8665u', '11800h', '10850h', '11850h', '1065g7', '1180g7', '10710u', '7500u', '10700u', '10700', '10700t', '10700f', '10700k', '10700kf', '10750h', '10870h', '10875h', '11900', '10900', '10900h', '10900f', '11900f', '10900k', '11900k', '11900h', '11980hk', '10980hk', '10885h', '10850k', '1115g4', '1125g4', '1135g7', '10310u', '11600f', '1130g7', '1145g7', '1145gre', '7200u', '11400h', '11370h', '1160g7', '11375h', '11400f', 'g5905t', '3865u', '11500t', '9500', '11500', 'g5905', 'n3060', 'n3160', '4216', '4210r', 'n4100', '10500h', '10600t', 'n2930', '7y57', '1165g7', '1165g', '11700', '11700t', '11700f', '11700kf', '11700k', '1185g7', '2100', '6100te', '2120', '5217', '2300x', '3250', '1115gre', '2700u', '5800x3d', '2400', '12600kf', '2950x', '3955wx', '3945wx', '5995wx', '5965wx', '5975wx', '5955wx', '5945wx', '5675u', '5500u', '3975wx', '2955u', '2990wx', '3050u', '3100', '3200g', '3250c', '3200ge', '3220', '10300t', '3200u', '5300g', '3300u', '3250u', '3300x', '3400g', '5600h', '4450u', '4600g', '5600u', '3427u', '3450u', '3470', '3500u', '10105t', '3050ge', 'tera2321', '3550h', '3500c', '3580uxx', '5650u', '3600', '3600x', '3700u', '5800u', '5750ge', '5750g', '3700c', '3700x', '3780u', '4750u', '3900', '3900x', '4300g', '4300u', '5425u', '5425c', '5350g', '5350ge', '10940x', '10900x', '10920x', '2200g', '4500u', 'r1305g', 'v1807b', '4570', '4570t', '10600', '13700k', '10500u', '4590', '3350g', '3400ge', '6600h', '6600hs', '6800h', '6800hs', '6900hx', '4600h', '4600u', '4650u', '4650ge', '4650g', '4680u', '4350g', '4350ge', '4700g', '4980u', '4750ge', '4750g', '4700u', '4770', '4800h', '4800hs', '4800u', '4900h', '4900hs', '5005u', '5200u', '5205u', 'n2840', 'n4500', '5257u', '5600x', '5800', '5800h', '5800x', '5700u', '5825u', '5850u', '5700g', '3750h', '5900', '5950x', '5900x', '5900hs', '5900hx', '5980hs', '6200u', '6300u', '6305', '6500', '6500t', '7300u', '7500', '7500t', '7700', '8650u', '7130u', '7100u', '7100', '8100', '8100t', '8145u', '11400t', '8145ue', '8100y', '8130u', '8265u', '8250u', '8365u', '1155g7', '8400', '8400t', '8500', '8500t', '8500y', '8700', '8750h', '9100', '9100f', '9100t', '12700k', '12700h', '12700', '9400', '9300h', '9400f', '9400t', '9600kf', '9600t', '8200y', 'l16g7', '9700', '8850h', '9700f', '9800x', '9700k', '9700t', '9750', '6242r', '9750h', '7820hq', '1195g7', '11390h', '11320h', '9900', '10900t', '5600g', '5600', '6600u', '9900t', '9900kf', '11900kf', '3020e', 'g620', '8505', 'g860', '6500y', 'g6400', 'g6400t', '4417u', '7505', '4425y', '6405u', 'j4005', 'j4105', 'j4025', 'j3355', '3867u', 'n3450', 'j5005', 'j5040', 'n5000', 'n5030', 'n6000', 'n3350', 'n4000', 'n4020', 'n5100', 'n4120', 'z8350', '3050e', '3050c', '3150u', '3150g', '3150c', '1110g4', '3145b', '300ge', 'v1756b', 'v1202b', 'v1605b', 'r1505g', '3995wx', '9120c', '9120e', '9120', '9125', '9220c', '9220e', '9425', 'mt8173c', 'mt8183', 'm8173c', 'p60t', 'rk3288', 'm1', '6242', '4214r', 'exynos', '1390p', 'n6005', 'mt8183c', '12450h', '6400', 'm2', '1240p', '1230u', 'g6900t', 'g6900', '12900', '12100t', '6650u', '6850u', '5450u', '8192', '1021u', '12900t', 'n4505', '1006g1', '1370p', '4108', '11500h', '11500b', '4210', '7260u', '6820eq', '7600u', '8350u', '11260h', '1245u', '8365ue', '9980hk', 'n5105', '5875u', '10100e', '11900kb', '9850h', '1265u', '12900f', '1250u', '12700p', '7305', '5300u', '10600k', '1075', '1250', '1250p', '1270', '1280p', '1290', '1290p', '12950hx', '2124g', '2225', '2245', '2400g', '3204', '3500', '3700', '420gi', '5218', '6226r', '6800hx', '6980hx', '7220u', '9500t', '9600', '9600k', 'g5420t', 'g6600', '11700b']
    return lst


# def dict_to_csv(csv_name: str, data: List[Dict]) -> bool:
#     """
#     Description:
#         - crate csv file for given data

#     Returns:
#         bool: boolean
#     """
#     try:
#         data = json.loads(json.dumps(data, indent = 4))
#         df = pd.DataFrame(data)
#         dt = datetime.today()
#         csv_name = '{}_{}_{}.csv'.format(csv_name, str(dt.day), str(dt.month))
#         df.to_csv(csv_name, index = False, encoding = 'utf-8')
#         return True
#     except:
#         return False

def get_brand_name(product_title: str) -> str:
    """
    Description:
        - return brand name if exist in product title

    Returns:
        str: brand name
    """
    brand_name_list = BRAND_LIST
    try:
        product_title = product_title.lower()
        for brand in brand_name_list:
            if re.search(brand, product_title):
                if brand == 'lenovo':
                    return 'lenovo united states inc'
                return brand
    except:
        return ''

def get_processor_model(title):
    product = title.lower()
    try:
        processor_type = get_processor_variants()
        modal = ''
        for modal_name in processor_type:
            modal = re.search(modal_name, product).group() if re.search(modal_name, product) else ''
            if modal != '':
                break
        return modal.strip('\n').strip()
    except:
        return ''

def get_processor_name(product_title: str) -> str:
    """
    Description:
        - match processor name and variant from title

    Returns:
        str: name, variant
    """
    try:
        if len(product_title) != 0 and product_title:
            product = product_title.lower()
            name = variant = ''
            if 'i3' in product:
                variant = 'i3'
                name = 'intel core'
            if 'i5' in product:
                variant = 'i5'
                name = 'intel core'
            if 'i7' in product:
                variant = 'i7'
                name = 'intel core'
            if 'i9' in product:
                variant = 'i9'
                name = 'intel core'
            if 'celeron' in product:
                variant = 'celeron'
                name = 'intel'
            if 'pentium' in product:
                variant = 'pentium'
                name = 'intel'
            if 'intel quad core' in product:
                variant = 'core'
                name = 'intel quad'
            if 'athlon' in product:
                variant = 'athlon'
                name = 'amd'
            if 'ryzen 3' in product:
                variant = '3'
                name = 'amd ryzen'
            if 'ryzen 5' in product:
                variant = '5'
                name = 'amd ryzen'
            if 'ryzen 7' in product:
                variant = '7'
                name = 'amd ryzen'
            if 'ryzen 9' in product:
                variant = '9'
                name = 'amd ryzen'
            if 'mediatek' in product:
                variant = 'm'
                name = 'mediatek'
            if re.search('AMD Ryzen\xe2\x84\xa2 3', product) and re.search('amd', product):
                variant = '3'
                name = 'amd ryzen'
            if re.search('amd ryzen threadripper', product) and re.search('amd', product):
                variant = 'threadripper'
                name = 'amd ryzen'
            if re.search('amd ryzen processor 7', product) and re.search('amd', product):
                variant = '7'
                name = 'amd ryzen'
            if re.search('amd fx', product) and re.search('amd', product):
                variant = 'fx'
                name = 'amd'
            if re.search('core 2 duo', product) and re.search('intel', product):
                variant = 'core 2 duo'
                name = 'intel'
            if re.search('core2 duo', product) and re.search('intel', product):
                variant = 'core 2 duo'
                name = 'intel'
            if re.search('quantum', product) and re.search('a7', product):
                variant = 'a7'
                name = 'quantum'
            if re.search('dual-core', product) and re.search('intel', product):
                variant = 'dual core'
                name = 'intel'
            if re.search('dual core', product) and re.search('intel', product):
                variant = 'dual core'
                name = 'intel'
            if re.search('intel xeon e5', product) and re.search('intel', product):
                variant = 'e5'
                name = 'intel xeon'
            if re.search('a6', product) and re.search('amd', product):
                variant = 'a6'
                name = 'amd'
            if re.search('a4', product) and re.search('amd', product):
                variant = 'a4'
                name = 'amd'
            if re.search('a8', product) and re.search('amd', product):
                variant = 'a8'
                name = 'amd'
            if re.search('a9', product) and re.search('amd', product):
                variant = 'a9'
                name = 'amd'
            if re.search('a12', product) and re.search('amd', product):
                variant = 'a12'
                name = 'amd'
            if re.search('a10', product) and re.search('amd', product):
                variant = 'a10'
                name = 'amd'
            if re.search('a12', product) and re.search('amd', product):
                variant = 'a12'
                name = 'amd'
            if re.search('r5', product) and re.search('amd', product):
                variant = '5'
                name = 'amd ryzen'
            if re.search('r3', product) and re.search('amd', product):
                variant = '3'
                name = 'amd ryzen'
            if re.search('r7', product) and re.search('amd', product):
                variant = '7'
                name = 'amd ryzen'
            if re.search('r3', product):
                variant = '3'
                name = 'amd ryzen'
            if re.search('r7', product):
                variant = '7'
                name = 'amd ryzen'
            if re.search('r5', product):
                variant = '5'
                name = 'amd ryzen'
            if re.search('r9', product):
                variant = '9'
                name = 'amd ryzen'
            if re.search('exynos', product) and re.search('samsung', product):
                variant = 'exynos'
                name = 'samsung'
            if re.search('macbook' , product) and re.search('apple' , product):
                variant = ' '
                name = 'm1'
            if name != '' and variant != '':
                return '{} {}'.format(name.lower(), variant.lower()).strip()
            else:
                return ''
    except:
        return ''


def sanitize_data(data: list) -> bool:
    """
    Description:
        - remove tags from data

    Returns:
        str: bool
    """
    if type(data) is list:
        try:
            sanitized_data = [remove_tags(item) for item in data]
            if len(sanitized_data) == 1:
                return sanitized_data[0]
        except:
            pass
    return False

def get_credentials():
    credential_path = '/srv/code/ecommerce-scrapy/gmail.json'
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print("Error")
    return credentials


def send_mail(subject,alert_msg,to):
    message = MIMEText(alert_msg)
    message['to'] = to
    message['from'] = "notifications@lyxellabs.com"
    message['subject'] = subject
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    mail_service = discovery.build('gmail', 'v1', http=http,cache_discovery=False)
    try:
        message = (mail_service.users().messages().send(userId="me", body={'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}).execute())
        print('Alert sent')
    except Exception as e:
        print("failed to send mail %s" % str(e))


####### processor_model ->  ['processor' , 'processor_type'] -- > ONLY MODEL NUMBERS WITH MOST ACCURATE MATCHING
####### Term based only 
pmodel_type_map = {
    "3600xt":["amd","amd ryzen 5"],
    "7600":["amd","amd ryzen 5"],
    "4500":["amd","amd ryzen 5"],
    "7950x3d":["amd","amd ryzen 9"],
    "7900x3d":["amd","amd ryzen 9"],
    "7900x":["amd","amd ryzen 9"],
    "7730u": ["amd", "amd ryzen 7"],
    "7530u": ["amd", "amd ryzen 5"],
    "7330u": ["amd", "amd ryzen 3"],
    "10900kf": ["intel", "intel core i9"],
    "13700kf": ["intel", "intel core i7"],
    "1135g4": ["intel", "intel core i5"],
    "1220p": ["intel", "intel core i3"],
    "7950x": ["amd", "amd ryzen 3"],
    "5300ge": ["amd", "amd ryzen 3"],
    "5600ge": ["amd", "amd ryzen 5"],
    "5650g": ["amd", "amd ryzen 5"],
    "r1606g": ["amd", "amd ryzen"],
    "5400u": ["amd", "amd ryzen 3"],
    "4600ge": ["amd", "amd ryzen 5"],
    "4300ge": ["amd", "amd ryzen 3"],
    "4700s": ["amd", "amd"],
    "5800hs": ["amd", "amd ryzen 7"],
    "3015ce": ["amd", "amd "],
    "5980hx": ["amd", "amd ryzen 9"],
    "4500m": ["amd", "amd a8"],
    "5350m": ["amd", "amd a8"],
    "2500u": ["amd", "amd ryzen 5"],
    "5625u": ["amd", "amd ryzen 5"],
    "5650ge": ["amd", "amd ryzen 5"],
    "9225": ["amd", "amd a6"],
    "3580u": ["amd", "amd ryzen 5"],
    "12700kf": ["intel", "intel core i7"],
    "j4125": ["intel", "intel celeron"],
    "12700f": ["intel", "intel core i7"],
    "12800h": ["intel", "intel core i7"],
    "1270p": ["intel", "intel core i7"],
    "5700": ["amd", "amd ryzen 7"],
    "5700x": ["amd", "amd ryzen 7"],
    "6700": ["intel", "intel core i7"],
    "10100f": ["intel", "intel core i3"],
    "5250u": ["intel", "intel core i5"],
    "5125c": ["amd", "amd ryzen 3"],
    "5500": ["amd", "amd ryzen 5"],
    "12700t": ["intel", "intel core i7"],
    "12100f": ["intel", "intel core i3"],
    "12400t": ["intel", "intel core i5"],
    "1255u": ["intel", "intel core i7"],
    "12650h": ["intel", "intel core i7"],
    "12900hk": ["intel", "intel core i9"],
    "12900hx": ["intel", "intel core i9"],
    "12800hx": ["intel", "intel core i7"],
    "6900hs": ["amd", "amd ryzen 9"],
    "1215u": ["intel", "intel core i3"],
    "1235u": ["intel", "intel core i5"],
    "4205u": ["intel", "intel pentium"],
    "g6405": ["intel", "intel pentium gold"],
    "5405u": ["intel", "intel pentium"],
    "8565u": ["intel", "intel core i7"],
    "1260p": ["intel", "intel core i7"],
    "1005g1": ["intel", "intel core i3"],
    "12100": ["intel", "intel core i3"],
    "12400": ["intel", "intel core i5"],
    "12500h": ["intel", "intel core i5"],
    "12500u": ["intel", "intel core i7"],
    "11950h": ["intel", "intel core i9"],
    "11950": ["intel", "intel core i9"],
    "10100": ["intel", "intel core i3"],
    "10100t": ["intel", "intel core i3"],
    "10105f": ["intel", "intel core i3"],
    "10105": ["intel", "intel core i3"],
    "10110u": ["intel", "intel core i3"],
    "10210u": ["intel", "intel core i5"],
    "10200h": ["intel", "intel core i5"],
    "12500": ["intel", "intel core i5"],
    "12500t": ["intel", "intel core i5"],
    "10300h": ["intel", "intel core i5"],
    "10300": ["intel", "intel core i3"],
    "1035g1": ["intel", "intel core i5"],
    "1035g7": ["intel", "intel core i5"],
    "10505": ["intel", "intel core i5"],
    "10400": ["intel", "intel core i5"],
    "1035g4": ["intel", "intel core i5"],
    "10400f": ["intel", "intel core i5"],
    "10400t": ["intel", "intel core i5"],
    "10500": ["intel", "intel core i5"],
    "10500t": ["intel", "intel core i5"],
    "11600k": ["intel", "intel core i5"],
    "12400f": ["intel", "intel core i5"],
    "n5095": ["intel", "intel celeron"],
    "12600": ["intel", "intel core i5"],
    "12900k": ["intel", "intel core i9"],
    "12900kf": ["intel", "intel core i9"],
    "12600k": ["intel", "intel core i5"],
    "11400": ["intel", "intel core i5"],
    "11600kf": ["intel", "intel core i5"],
    "12900h": ["intel", "intel core i9"],
    "10510u": ["intel", "intel core i7"],
    "10810u": ["intel", "intel core i7"],
    "10600kf": ["intel", "intel core i5"],
    "1140g7": ["intel", "intel core i5"],
    "11300h": ["intel", "intel core i5"],
    "8635u": ["intel", "intel core i5"],
    "10610u": ["intel", "intel core i7"],
    "8665u": ["intel", "intel core i7"],
    "11800h": ["intel", "intel core i7"],
    "10850h": ["intel", "intel core i7"],
    "11850h": ["intel", "intel core i7"],
    "1065g7": ["intel", "intel core i7"],
    "1180g7": ["intel", "intel core i7"],
    "10710u": ["intel", "intel core i7"],
    "7500u": ["intel", "intel core i7"],
    "10700u": ["intel", "intel core i7"],
    "10700": ["intel", "intel core i7"],
    "10700t": ["intel", "intel core i7"],
    "10700f": ["intel", "intel core i7"],
    "10700k": ["intel", "intel core i7"],
    "10700kf": ["intel", "intel core i7"],
    "10750h": ["intel", "intel core i7"],
    "10870h": ["intel", "intel core i7"],
    "10875h": ["intel", "intel core i7"],
    "11900": ["intel", "intel core i9"],
    "10900": ["intel", "intel core i9"],
    "10900h": ["intel", "intel core i9"],
    "10900f": ["intel", "intel core i9"],
    "11900f": ["intel", "intel core i9"],
    "10900k": ["intel", "intel core i9"],
    "11900k": ["intel", "intel core i9"],
    "11900h": ["intel", "intel core i9"],
    "11980hk": ["intel", "intel core i9"],
    "10980hk": ["intel", "intel core i9"],
    "10885h": ["intel", "intel core i9"],
    "10850k": ["intel", "intel core i9"],
    "1115g4": ["intel", "intel core i3"],
    "1125g4": ["intel", "intel core i3"],
    "1135g7": ["intel", "intel core i5"],
    "10310u": ["intel", "intel core i5"],
    "11600f": ["intel", "intel core i5"],
    "1130g7": ["intel", "intel core i5"],
    "1145g7": ["intel", "intel core i5"],
    "1145gre": ["intel", "intel core i5"],
    "7200u": ["intel", "intel core i5"],
    "11400h": ["intel", "intel core i5"],
    "11370h": ["intel", "intel core i7"],
    "1160g7": ["intel", "intel core i7"],
    "11375h": ["intel", "intel core i7"],
    "11400f": ["intel", "intel core i5"],
    "g5905t": ["intel", "intel celeron"],
    "3865u": ["intel", "intel celeron"],
    "11500t": ["intel", "intel core i5"],
    "9500": ["intel", "intel core i5"],
    "11500": ["intel", "intel core i5"],
    "g5905": ["intel", "intel celeron"],
    "n3060": ["intel", "intel celeron"],
    "n3160": ["intel", "intel celeron"],
    "4216": ["intel", "intel xeon silver"],
    "4210r": ["intel", "intel xeon silver"],
    "n4100": ["intel", "intel celeron"],
    "10500h": ["intel", "intel core i5"],
    "10600t": ["intel", "intel core i5"],
    "n2930": ["intel", "intel celeron"],
    "7y57": ["intel", "core i5"],
    "n5105" : ["intel", "intel celeron"],
    "8279u": ["intel", "core i5"],
    "8279": ["intel", "core i5"],
    "j3455": ["intel", "intel celeron"],
    "4590t":["intel", "core i5"],
    "j4205": ["intel", "core i5"],
    "3770": ["intel", "intel core i7"],
    "1165g7": ["intel", "intel core i7"],
    "1165g": ["intel", "intel core i7"],
    "11700": ["intel", "intel core i7"],
    "11700t": ["intel", "intel core i7"],
    "11700f": ["intel", "intel core i7"],
    "11700kf": ["intel", "intel core i7"],
    "11700k": ["intel", "intel core i7"],
    "1185g7": ["intel", "intel core i7"],
    "2100": ["intel", "intel core i3"],
    "6100te": ["intel", "intel core i3"],
    "2120": ["intel", "intel core i3"],
    "5217": ["intel", "intel xeon gold"],
    "2300x": ["amd", "amd ryzen 3"],
    "3250": ["amd", "amd ryzen 3"],
    "1115gre": ["intel", "intel core i3"],
    "2700u": ["amd", "amd ryzen 7"],
    "5800x3d": ["amd", "amd ryzen 7"],
    "2400": ["intel", "intel core i5"],
    "12600kf": ["intel", "intel core i5"],
    "2950x": ["amd", "amd threadripper"],
    "3955wx": ["amd", "amd threadripper"],
    "3945wx": ["amd", "amd threadripper"],
    "5995wx": ["amd", "amd threadripper"],
    "5965wx": ["amd", "amd threadripper"],
    "5975wx": ["amd", "amd threadripper"],
    "5955wx": ["amd", "amd threadripper"],
    "5945wx": ["amd", "amd threadripper"],
    "5675u": ["amd", "amd ryzen 5 pro"],
    "5500u": ["amd", "amd ryzen 5"],
    "3975wx": ["amd", "amd threadripper pro"],
    "2955u": ["intel", "intel celeron"],
    "2990wx": ["amd", "amd threadripper"],
    "3050u": ["amd", "amd athlon silver"],
    "3100": ["amd", "amd ryzen 3"],
    "3200g": ["amd", "amd ryzen 3"],
    "3250c": ["amd", "amd ryzen 3"],
    "3200ge": ["amd", "amd ryzen 3"],
    "3220": ["intel", "intel core i3"],
    "10300t": ["intel", "intel core i3"],
    "3200u": ["amd", "amd ryzen 3"],
    "5300g": ["amd", "amd ryzen 3"],
    "3300u": ["amd", "amd ryzen 3"],
    "3250u": ["amd", "amd ryzen 3"],
    "3300x": ["amd", "amd ryzen 3"],
    "3400g": ["amd", "amd ryzen 5"],
    "5600h": ["amd", "amd ryzen 5"],
    "4765t":["intel", "intel core i7"],
    "4450u": ["amd", "amd ryzen 5"],
    "4600g": ["amd", "amd ryzen 5"],
    "5600u": ["amd", "amd ryzen 5"],
    "3427u": ["intel", "intel core i5"],
    "3450u": ["amd", "amd ryzen 5"],
    "3470": ["intel", "intel core i5"],
    "3500u": ["amd", "amd ryzen 5"],
    "10105t": ["intel", "intel core i3"],
    "3050ge": ["amd", "amd athlon sliver"],
    "tera2321": ["teradici", "tera2321"],
    "3550h": ["amd", "amd ryzen 5"],
    "3500c": ["amd", "amd ryzen 5"],
    "3580uxx": ["amd", "amd ryzen 5 surface edition"],
    "5650u": ["amd", "amd ryzen 5"],
    "3600": ["amd", "amd ryzen 5"],
    "3600x": ["amd", "amd ryzen 5"],
    "3700u": ["amd", "amd ryzen 7"],
    "5800u": ["amd", "amd ryzen 7"],
    "5750ge": ["amd", "amd ryzen 7"],
    "5750g": ["amd", "amd ryzen 7"],
    "3700c": ["amd", "amd ryzen 7"],
    "3700x": ["amd", "amd ryzen 7"],
    "3780u": ["amd", "amd ryzen 7 surface edition"],
    "4750u": ["amd", "amd ryzen 7 pro"],
    "3900": ["amd", "amd ryzen 9"],
    "3900x": ["amd", "amd ryzen 9"],
    "4300g": ["amd", "amd ryzen 3"],
    "4300u": ["amd", "amd ryzen 3"],
    "5425u": ["amd", "amd ryzen 3"],
    "5425c": ["amd", "amd ryzen 3"],
    "5350g": ["amd", "amd ryzen 3"],
    "5350ge": ["amd", "amd ryzen 3"],
    "10940x": ["intel", "intel core i9"],
    "10900x": ["intel", "intel core i9"],
    "10920x": ["intel", "intel core i9"],
    "2200g": ["amd", "amd ryzen 3"],
    "4500u": ["amd", "amd ryzen 5"],
    "r1305g": ["amd", "amd ryzen embedded"],
    "v1807b": ["amd", "amd ryzen embedded"],
    "4570": ["intel", "intel core i5"],
    "4570t": ["intel", "intel core i5"],
    "10600": ["intel", "intel core i5"],
    "13700k": ["intel", "intel core i7"],
    "10500u": ["intel", "intel core i5"],
    "4590": ["intel", "intel core i5"],
    "3350g": ["amd", "amd ryzen 5"],
    "3400ge": ["amd", "amd ryzen 5"],
    "6600h": ["amd", "amd ryzen 5"],
    "6600hs":["amd", "amd ryzen 5"],
    "6800h": ["amd", "amd ryzen 7"],
    "6800hs": ["amd", "amd ryzen 7"],
    "6900hx": ["amd", "amd ryzen 9"],
    "4600h": ["amd", "amd ryzen 5"],
    "4600u": ["amd", "amd ryzen 5"],
    "4650u": ["amd", "amd ryzen 5"],
    "4650ge": ["amd", "amd ryzen 5"],
    "4650g": ["amd", "amd ryzen 5 pro"],
    "4680u": ["amd", "amd ryzen 5"],
    "4350g": ["amd", "amd ryzen 3 pro"],
    "4350ge": ["amd", "amd ryzen 3 pro"],
    "4700g": ["amd", "amd ryzen 7"],
    "4980u": ["amd", "amd ryzen 7"],
    "4750ge": ["amd", "amd ryzen 7"],
    "4750g": ["amd", "amd ryzen 7"],
    "4700u": ["amd", "amd ryzen 7"],
    "4770": ["intel", "intel core i7"],
    "4800h": ["amd", "amd ryzen 7"],
    "4800hs": ["amd", "amd ryzen 7"],
    "4800u": ["amd", "amd ryzen 7"],
    "4800s": ["amd", "amd ryzen 7"],
    "4900h": ["amd", "amd ryzen 9"],
    "4900hs": ["amd", "amd ryzen 9"],
    "5005u": ["intel", "intel core i3"],
    "5200u": ["intel", "intel core i5"],
    "5205u": ["intel", "intel celeron"],
    "n2840": ["intel", "intel celeron"],
    "n4500": ["intel", "intel celeron"],
    "5257u": ["intel", "intel core i5"],
    "5600x": ["amd", "amd ryzen 5"],
    "5800": ["amd", "amd ryzen 7"],
    "5800h": ["amd", "amd ryzen 7"],
    "5800x": ["amd", "amd ryzen 7"],
    "5700u": ["amd", "amd ryzen 7"],
    "5825u": ["amd", "amd ryzen 7"],
    "5850u": ["amd", "amd ryzen 7"],
    "5700g": ["amd", "amd ryzen 7"],
    "3750h": ["amd", "amd ryzen 7"],
    "5900": ["amd", "amd ryzen 9"],
    "5950x": ["amd", "amd ryzen 9"],
    "5900x": ["amd", "amd ryzen 9"],
    "5900hs": ["amd", "amd ryzen 9"],
    "5900hx": ["amd", "amd ryzen 9"],
    "5980hs": ["amd", "amd ryzen 9"],
    "6200u": ["intel", "intel core i5"],
    "6300u": ["intel", "intel core i5"],
    "6305": ["intel", "intel celeron"],
    "6500": ["intel", "intel core i5"],
    "6500t": ["intel", "intel core i5"],
    "7300u": ["intel", "intel core i5"],
    "7500": ["intel", "intel core i5"],
    "7500t": ["intel", "intel core i5"],
    "7700": ["intel", "intel core i7"],
    "8650u": ["intel", "intel core i7"],
    "7130u": ["intel", "intel core i3"],
    "7100u": ["intel", "intel core i3"],
    "7100": ["intel", "intel core i3"],
    "8100": ["intel", "intel core i3"],
    "8109u":["intel", "intel core i3"],
    "8100t": ["intel", "intel core i3"],
    "8145u": ["intel", "intel core i3"],
    "11400t": ["intel", "intel core i5"],
    "8145ue": ["intel", "intel core i3"],
    "8100y": ["intel", "intel core m3"],
    "8130u": ["intel", "intel core i3"],
    "8265u": ["intel", "intel core i5"],
    "8250u": ["intel", "intel core i5"],
    "8365u": ["intel", "intel core i5"],
    "1155g7": ["intel", "intel core i5"],
    "8400": ["intel", "intel core i5"],
    "8400t": ["intel", "intel core i5"],
    "8500": ["intel", "intel core i5"],
    "8500t": ["intel", "intel core i5"],
    "8500y": ["intel", "intel core i5"],
    "8700": ["intel", "intel core i7"],
    "8750h": ["intel", "intel core i7"],
    "9100": ["intel", "intel core i3"],
    "9100f": ["intel", "intel core i3"],
    "9100t": ["intel", "intel core i3"],
    "12700k": ["intel", "intel core i7"],
    "12700h": ["intel", "intel core i7"],
    "12700": ["intel", "intel core i7"],
    "9400": ["intel", "intel core i5"],
    "9300h": ["intel", "intel core i5"],
    "9400f": ["intel", "intel core i5"],
    "9400t": ["intel", "intel core i5"],
    "9600kf": ["intel", "intel core i5"],
    "9600t": ["intel", "intel core i5"],
    "8200y": ["intel", "intel core i5"],
    "l16g7": ["intel", "intel core i5"],
    "9700": ["intel", "intel core i7"],
    "8850h": ["intel", "intel core i7"],
    "9700f": ["intel", "intel core i7"],
    "9800x": ["intel", "intel core i7"],
    "9700k": ["intel", "intel core i7"],
    "9700t": ["intel", "intel core i7"],
    "9750": ["intel", "intel core i7"],
    "6242r": ["intel", "intel xeon gold"],
    "9750h": ["intel", "intel core i7"],
    "7820hq": ["intel", "intel core i7"],
    "1195g7": ["intel", "intel core i7"],
    "11390h": ["intel", "intel core i7"],
    "11320h": ["intel", "intel core i5"],
    "9900": ["intel", "intel core i9"],
    "10900t": ["intel", "intel core i9"],
    "5600g": ["amd", "amd ryzen 5"],
    "5600": ["amd", "amd ryzen 5"],
    "6600u": ["intel", "intel core i7"],
    "9900t": ["intel", "intel core i9"],
    "9900kf": ["intel", "intel core i9"],
    "11900kf": ["intel", "intel core i9"],
    "3020e": ["amd", "amd 3020e"],
    "g620": ["intel", "intel pentium"],
    "8505": ["intel", "intel pentium"],
    "g860": ["intel", "intel pentium"],
    "6500y": ["intel", "intel pentium gold"],
    "g6400": ["intel", "intel pentium gold"],
    "g6400t": ["intel", "intel pentium gold"],
    "4417u": ["intel", "intel pentium gold"],
    "7505": ["intel", "intel pentium gold"],
    "4425y": ["intel", "intel pentium gold"],
    "6405u": ["intel", "intel pentium gold"],
    "j4005": ["intel", "intel celeron"],
    "j4105": ["intel", "intel celeron"],
    "j4025": ["intel", "intel celeron"],
    "j3355": ["intel", "intel celeron"],
    "3867u": ["intel", "intel celeron"],
    "n3450": ["intel", "intel celeron"],
    "j5005": ["intel", "intel pentium silver"],
    "j5040": ["intel", "intel pentium silver"],
    "n5000": ["intel", "intel pentium silver"],
    "n5030": ["intel", "intel pentium silver"],
    "n6000": ["intel", "intel pentium silver"],
    "n3350": ["intel", "intel celeron"],
    "n4000": ["intel", "intel celeron n"],
    "n4020": ["intel", "intel celeron"],
    "n5100": ["intel", "intel celeron n"],
    "n4120": ["intel", "intel celeron n"],
    "z8350": ["intel", "intel atom"],
    "3050e": ["amd", "amd athlon silver"],
    "3050c": ["amd", "amd athlon silver"],
    "3150u": ["amd", "amd athlon gold"],
    "3150g": ["amd", "amd athlon gold"],
    "3150c": ["amd", "amd athlon gold"],
    "1110g4": ["intel", "intel core i3"],
    "3145b": ["amd", "amd athlon pro"],
    "300ge": ["amd", "amd athlon pro"],
    "v1756b": ["amd", "amd ryzen embedded"],
    "v1202b": ["amd", "amd ryzen embedded"],
    "v1605b": ["amd", "amd ryzen embedded"],
    "r1505g": ["amd", "amd ryzen embedded"],
    "3995wx": ["amd", "amd threadripper"],
    "9120c": ["amd", "amd a4"],
    "9120e": ["amd", "amd a4"],
    "9120": ["amd", "amd a4"],
    "9125": ["amd", "amd a4"],
    "8770e": ["amd", "amd a4"],
    "9220c": ["amd", "amd a6"],
    "9220e": ["amd", "amd a6"],
    "8570e": ["amd", "amd a6"],
    "9425": ["amd", "amd a9"],
    "mt8173c": ["mediatek", "mediatek"],
    "mt8183": ["mediatek", "mediatek"],
    "m8173c": ["mediatek", "mediatek"],
    "p60t": ["mediatek", "mediatek helio"],
    "rk3288": ["rocketchip", "rocketchip cortex a17"],
    "m1": ["apple", "apple m1"],
    "6242": ["intel", "intel xeon gold"],
    "4214r": ["intel", "intel xeon silver"],
    "exynos": ["samsung", "samsung exynos"],
    "1390p": ["intel", "intel xeon w"],
    "n6005": ["intel", "intel pentium"],
    "mt8183c": ["mediatek", "mediatek"],
    "12450h": ["intel", "intel core i5"],
    "6400": ["intel", "intel core i5"],
    "m2": ["apple", "apple m2"],
    "1240p": ["intel", "intel core i5"],
    "1230u": ["intel", "intel core i5"],
    "g6900t": ["intel", "intel celeron"],
    "g6900": ["intel", "intel celeron"],
    "12900": ["intel", "intel core i9"],
    "12100t": ["intel", "intel core i3"],
    "6650u": ["amd", "amd ryzen 5 pro"],
    "6850u": ["amd", "amd ryzen 7 pro"],
    "5450u": ["amd", "amd ryzen 3 pro"],
    "8192": ["mediatek", "mediatek kompanio"],
    "1021u": ["intel ", "intel core i5"],
    "12900t": ["intel ", "intel core i9"],
    "n4505": ["intel", "intel celeron"],
    "1006g1": ["intel ", "intel core i3"],
    "1370p": ["intel ", "intel xeon w"],
    "4108": ["intel", "intel xeon silver"],
    "11500h": ["intel", "intel core i5"],
    "11500b": ["intel", "intel core i5"],
    "4210": ["intel", "intel xeon"],
    "7260u": ["intel", "intel core i5"],
    "6820eq": ["intel", "intel core i7"],
    "7600u": ["intel", "intel core i7"],
    "8350u": ["intel", "intel core i5"],
    "11260h": ["intel", "intel core i5"],
    "1245u": ["intel", "intel core i5"],
    "8365ue": ["intel", "intel core i5"],
    "9980hk": ["intel", "intel core i9"],
    "n5105": ["intel", "intel celeron"],
    "5875u": ["amd", "amd ryzen 7 pro"],
    "10100e": ["intel", "intel core i3"],
    "10100": ["intel", "intel core i3"],
    "11900kb": ["intel", "intel core i9"],
    "9850h": ["intel", "intel core i7"],
    "1265u": ["intel", "intel core i7"],
    "12900f": ["intel", "intel core i9"],
    "1250u": ["intel", "intel core i7"],
    "12700p": ["intel", "intel core i7"],
    "7305": ["intel", "intel celeron"],
    "5300u": ["amd", "amd ryzen 3"],
    "10600k": ["intel", "intel core i5"],
    "1075": ["intel", "intel core i7"],
    "1250": ["intel", "intel xeon w"],
    "1250p": ["intel", "intel core i5"],
    "1270": ["intel", "intel core i7"],
    "12700t": ["intel", "intel core i7"],
    "1280p": ["intel", "intel core i7"],
    "1290": ["intel", "intel core i9"],
    "1290p": ["intel", "intel xeon w"],
    "12950hx": ["intel", "intel core i9"],
    "2124g": ["intel", "intel xeon"],
    "2225": ["intel", "intel xeon w"],
    "2245": ["intel", "intel xeon w"],
    "2400g": ["amd", "amd ryzen 5"],
    "3204": ["intel", "intel xeon bronze"],
    "3500": ["amd", "amd ryzen 5"],
    "3700": ["amd", "amd ryzen 7 pro"],
    "420gi": ["amd", "amd"],
    "7600x": ["amd", "amd ryzen 7"],
    "7700x": ["amd", "amd ryzen 7"],
    "5218": ["intel", "intel 2x xeon"],
    "6226r": ["intel", "intel xeon gold"],
    "6800hx": ["amd", "amd ryzen 9"],
    "6980hx": ["amd", "amd ryzen 9"],
    "7220u": ["amd", "amd athlon gold"],
    "6500u": ["intel", "intel core i7"],
    "9500t": ["intel", "intel core i5"],
    "9600": ["intel", "intel core i5"],
    "9600k": ["intel", "intel core i5"],
    "g5420t": ["intel", "intel pentium gold"],
    "g6600": ["intel", "intel pentium gold"],
    "11700b": ["intel", "intel core i7"],
    "7945hx": ["amd", "amd ryzen 9"],
    "7940hs": ["amd", "amd ryzen 9"],
    "6860z": ["amd", "amd ryzen 7 pro"],
    "8259u": ["intel", "intel core i5"],
    "7520u": ["amd", "amd ryzen 5"],
    "6157u": ["intel", "intel core i3"],
    "n4020c": ["intel", "intel celeron"],
    "6800u": ["amd", "amd ryzen 7"],
    "5560u": ["amd", "amd ryzen 5"],
    "13400" : ["intel", "intel core i5"],
    "13400f" : ["intel", "intel core i5"],
    "1340p" : ["intel", "intel core i5"],
    "rx-8120": ["amd", "amd rx-8120"],
    "13100": ["intel", "intel core i3"],
    "13900h" : ["intel", "intel core i9"], 
    "13900hx" : ["intel", "intel core i9"],
    "13650hx" : ["intel", "intel core i7"],
    "13700hx" : ["intel", "intel core i7"],
    "13700f" : ["intel", "intel core i7"],
    "13500hx" : ["intel", "intel core i5"],
    "13980hx" : ["intel", "intel core i9"],
    "13700h" : ["intel", "intel core i7"],
    "13500h" : ["intel", "intel core i5"],
    "7735h": ["amd","amd ryzen 7"],
    "7735hs": ["amd","amd ryzen 7"],
    "2100": ["amd", "amd ryzen 3 pro"],
    "a3050u": ["amd", "amd athlon silver"],
    "200ge": ["amd", "amd athlon"],
    "6850hs": ["amd", "amd ryzen 7 pro"],
    "6650h": ["amd", "amd ryzen 5 pro"],
    "n3050c": ["amd", "amd athlon"]
}
phrase_map = {    
        "gx 212jj" : [ 'amd' , 'amd embedded g-series' ],
        "gx 215jj" : [ 'amd' , 'amd embedded g-series' ],
        "gx 215jc": [ 'amd' , 'amd embedded g-series' ],
        "gx 215jj": [ 'amd' , 'amd embedded g-series' ],
        "w 1250": [ 'intel' , 'intel xeon w' ],
        "w 2245": [ 'intel' , 'intel xeon w' ],
        "xw1250": [ 'intel' , 'intel xeon w' ],
        #####   Seggregate phrase based matching
        ### matched with space as small terms might get false positive matches too 
        " sq1":  [ 'microsoft' , 'microsoft sq1' ],
        " sq2":  [ 'microsoft' , 'microsoft sq2' ],
        " 855":  [ 'qualcomm' , 'snapdragon' ],
        "xeon w": [ 'intel' , 'intel xeon w' ],
        " 7c ": [ 'qualcomm' , 'snapdragon' ],
        "x4 950": [ 'amd' , 'amd athlon' ],
        }
######## FOR MISSES IN L1 ONLY - PROVIDES PARTIAL DATA ONLY (i.e. No processor model)
######## include logic for default processor model if required
l2_pmodel_type_map = {
    " a4": [ 'amd' , 'amd a4' ],
    " a6": [ 'amd' , 'amd a4' ],
    " a8":[ 'amd' , 'amd a4' ],
    " a10": [ 'amd' , 'amd a4' ],
    " a12": [ 'amd' , 'amd a4' ],
    " r3": [ 'amd' , 'amd ryzen 3' ],
    " r5": [ 'amd' , 'amd ryzen 5' ],
    " r7": [ 'amd' , 'amd ryzen 7' ],
    " r9": [ 'amd' , 'amd ryzen 9' ],
    "ryzen 3": [ 'amd' , 'amd ryzen 3' ],
    "ryzen 5": [ 'amd' , 'amd ryzen 5' ],
    "ryzen 7": [ 'amd' , 'amd ryzen 7' ],
    "ryzen 9": [ 'amd' , 'amd ryzen 9' ],
    " i3": [ 'intel' , 'intel core i3' ],
    " i5": [ 'intel' , 'intel core i5' ],
    " i7": [ 'intel' , 'intel core i7' ],
    " i9": [ 'intel' , 'intel core i9' ],
    " duo": [ 'intel' , 'intel core 2 duo' ],
    "celeron": [ 'intel' , 'intel celeron' ],
    "atom": [ 'intel' , 'intel atom' ],
    "core m3": [ 'intel' , 'intel core m3' ],
    "xeon": [ 'intel' , 'intel xeon' ],
    "pentium": [ 'intel' , 'intel pentium' ],
    "athlon": [ 'amd' , 'amd athlon' ],
    "threadripper" : [ 'amd', 'amd threadripper'],
    "v1756b" : ["amd","amd ryzen embedded"],
    "v1202b" : ["amd","amd ryzen embedded"],
    "v1605b" : ["amd","amd ryzen embedded"],
    "3995wx" : [ 'amd', 'amd threadripper'],
    "g series embedded" : [ 'amd','amd embedded g-series' ],
    "2100ge" : ['amd', 'amd ryzen 3 pro'],
    "7120u" : ['amd', 'amd athlon silver'],
} 
########  MATCH WITH THE SUBKEYS FOR MORE ACCURATE MATCHING IN CASE OF MULTI REFRENCES 
########  PUT PREFRENCE None for groups which default processor_model values shouldnt be picked by default 
multi_refrences = {
        "3320m":  {'intel':[ 'intel' , 'intel core i5' ], 'amd' : [ 'amd' , 'amd a4' ] , '__prefrence__' : 'intel'},
        "9500":  {'intel':[ 'intel' , 'intel core i5' ], 'amd' : [ 'amd' , 'amd a6' ] , '__prefrence__' : 'intel'},
        "4130":  {'intel':[ 'intel' , 'intel core i3' ], 'amd' : [ 'amd' , 'amd fx' ],  '__prefrence__' : 'intel'},
        "4300m":  {'intel':[ 'intel' , 'intel core i5' ], 'amd' : [ 'amd' , 'amd a4' ], '__prefrence__' : 'intel'},
        "gold" :  {'pentium':[ 'intel' , 'intel pentium gold' ], 'athlon' : [ 'amd' , 'amd athlon gold' ],'xeon' : [ 'intel' , 'intel xeon gold' ], '__prefrence__' : None},
        "silver" : {'pentium':[ 'intel' , 'intel pentium silver' ], 'athlon' : [ 'amd' , 'amd athlon silver' ],'xeon' : [ 'intel' , 'intel xeon silver' ], '__prefrence__' : None},
        "5300u" : {'intel':[ 'intel' , 'intel core i5' ], 'amd' : [ 'amd' , 'amd ryzen 3' ] , '__prefrence__' : 'amd'}
}
term_keys = list(pmodel_type_map.keys())
phrase_keys = list(phrase_map.keys())
l2_models = list(l2_pmodel_type_map.keys())
multi_refrences_keys = list(multi_refrences.keys())

###### PROCESSING START HERE ( ) ##################
######  matching order 
###  1 :- term with split
###  2 :- Phrase with in
###  3 :- Multi reference keys
###  4 :- partial match with level 2 map
 
def squeeze_processor_info(input_text):
    try:
        input_text = input_text.lower()
        input_text = input_text.replace('-', ' ')
        input_text = input_text.replace('window', ' ').replace('with', ' ').replace('white', ' ')
        input_text= input_text.encode('ascii' , 'ignore').decode()
        match = False
        complete_match = False
        processor_model , processor, processor_type = None, None, None
        for model in term_keys:
            if model in input_text.split():
                match = True
                complete_match = True
                processor_model = model
                processor , processor_type = pmodel_type_map[model][0], pmodel_type_map[model][1]
                break
        if match == False and complete_match == False:
            for model in phrase_keys:
                if model in input_text:
                    match = True
                    complete_match = True
                    processor_model = model
                    processor , processor_type = phrase_map[model][0], phrase_map[model][1]
                    break

        if match == False:
            for key in multi_refrences_keys:
                if key in input_text:
                    second_term_candidates = list(multi_refrences[key].keys())
                    for candidate in second_term_candidates:
                        if candidate in input_text:
                            complete_match = True
                            match = True
                            processor_model = key if key not in ['gold', 'silver'] else ''
                            processor , processor_type = multi_refrences[key][candidate][0], multi_refrences[key][candidate][1]
                            break
                    if not complete_match:
                        preference = multi_refrences[key]['__prefrence__']
                        if preference :
                            match = True
                            processor_model = key if key not in ['gold', 'silver'] else ''
                            processor = multi_refrences[key][preference][0]
                            processor_type = multi_refrences[key][preference][1]

        if match == False:
            for l2_model in l2_models:
                if l2_model in input_text:
                    match = True
                    processor_model = ''
                    processor , processor_type = l2_pmodel_type_map[l2_model][0], l2_pmodel_type_map[l2_model][1]
                    break
                        
        response = {
            'processor' : '' if not processor else  processor.strip() ,
            'processor_type' : '' if not processor_type else  processor_type.strip() ,
            'processor_model' : '' if not processor_model else  processor_model.strip() ,
            'match' : match,
            'complete_match' : complete_match,
        }

        return response   
    except Exception as e:
        l.error("Exception in squeeze processor info")
        exc_type, exc_obj, exc_tb  = sys.exc_info()
        l.error( str(exc_type) + ' ---> ' + str(exc_tb.tb_lineno)  +'--->'+ str(exc_obj) )
        l.error('In string --> {}'.format(input_text))
        raise e


def status_function(spider_name,status,msg, job_id=None, info=None):
    StatusReporting(spider_name = spider_name ,status = status, message= msg, info=info, job_id=job_id).save()


def status_update_function(job_id, status, msg=None, eta=None):

    if msg and not eta:
        RequestInfo.objects(job_id=job_id).update(set__status=status, set__message=msg)
    elif msg and eta:
        RequestInfo.objects(job_id=job_id).update(set__status=status, set__message=msg, set__eta = eta)


def extract_processor_model(processor_text:str) -> str:
    pattern = re.compile(r"[a-zA-Z]*([0-9]{4,})[a-zA-Z]*")
    matched = re.search(pattern, processor_text)
    if matched:
        if not '{} series'.format(matched.group()) in processor_text:
            return matched.group()


def is_count_zero_or_not(data):
    status = "succeded"
    flag = any([ True if item.get('total_count') else False for item in data])
    if not flag:
        status = "failed"
    return status

def get_gpu_specs(data):
    map_list = ['amd','intel','nvidia','m1','arm']
    map_di = {
        'geforce':'nvidia',
        'radeon':'amd'
    }
    map_list1 = ['geforce','radeon']
    for item in map_list:
        if item in data:
            return item
    for item in map_list1:
        if item in data:
            return map_di[item]
    return ''

def get_url(url, header, proxy, retries=25):
    """
    Request url with proxy and custom header
    """
    data = False
    with requests.Session() as s:
        for i in range(1, retries):
            print("Retry: {} : link :{}".format(str(i), url))
            response = s.get(url, headers=header, proxies=proxy, verify = False)
            if response.status_code == 200 and len(response.content) > 2000:
                data = response
                print("Success")
                break
    return data


def get_url_without_proxy(url):
    """
    Request url without using proxy
    """
    data = False
    # with requests.Session() as s:
    for i in range(1, 5):
        print("Without Proxy Retry: ",str(i))
        response = requests.get(url)
        if response.status_code == 200:
            data = response
            print("Success")
            break
    return data

def check_sos_data(data):
    info = {}
    if not any([ True if item.get('total_count') else False for item in data]):
        info['summary'] = "All ZERO total_count"
    return yaml.dump(info)

def prred(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prgreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def pryellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prcyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prlightgray(skk): print("\033[97m {}\033[00m" .format(skk))

def sanitize_string(input_text):
    '''
    To Remove special characters from input_text
    '''
    return ' '.join(input_text.strip().encode("ascii","ignore").decode().split())

class ValidateScrapedData:
    """
    Validate the Scraped Data 

    Parameters
    ----------
    data = Accepts List of dict

    fields = In which data will be validated
                default fields are: ['link', 'product_name', 'reviews', 'item_id', 'price', 
                'ratings', 'image_count', 'order', 'page_count', 'page', 'offer', 'segment', 'brand_name', 
                'processor', 'processor_type', 'processor_model', 'gpu', 'gpu_type', 'item_category', 'website', 
                'timestamp']

    segments = In which segments you want to validate the data
                default fields are: ['consumer', 'commercial']

    field_ignore = Exclude fields for checking empty values
                    default value is: []

    retail_section = bool, default False
                Determines if the passed-in retail category_section or not:
                - If ``True``, assumes the passed-in category_section True and will run category_run() funtion 
                                        and exclude (segment) field from fields
                - If ``False``, assumes the passed-in category_run() funtion will not run

    category_section = bool, default False
                Determines if the passed-in category_section or not:
                - If ``True``, assumes the passed-in category_section True and will run category_run() funtion
                - If ``False``, assumes the passed-in category_run() funtion will not run

    sov_section = bool, default False
                Determines if the passed-in category_section or not:
                - If ``True``, assumes the passed-in sov_section True and will run sov_run() funtion
                - If ``False``, assumes the passed-in sov_run() funtion will not run

    sov_count = Accepts List of dict
                If sov_section is True, sov_count must not be empty (it will check sov_count)

    yaml_dump = bool, default False
                Determines if the passed-in category_section or not:
                - If ``True``, assumes the passed-in yaml_dump True and 
                                will Serialize the Python object/data into a YAML stream and return it.
                - If ``False``, assumes that don't serialize the Python object/data into a YAML stream.
    """

    def __init__(self, 
                data,
                fields=None, 
                segments=None, 
                field_ignore=[], 
                retail_section=False, 
                category_section=False, 
                sov_section=False, 
                sov_count=[], 
                yaml_dump=False
                ) -> None:
        self.data = data
        self.fields = ['link', 'product_name', 'reviews', 'item_id', 'price', 'ratings', 'image_count', 'order', 
                        'page_count', 'page', 'offer', 'segment', 'brand_name', 'processor', 'processor_type', 
                        'processor_model', 'gpu', 'gpu_type', 'item_category', 'website', 'timestamp']
        self.sov_fields = ['item_category','website','location','link','processor_model','timestamp',
                            'processor_type','item_id','product_name']
        self.categories = ['laptop', 'desktop', 'neither']
        self.segments = ['consumer', 'commercial']
        self.field_ignore = field_ignore
        self.retail_section = retail_section
        self.category_section = category_section
        self.sov_section = sov_section
        self.sov_count = sov_count
        self.yaml_dump = yaml_dump
        if fields:
            self.fields = fields
        if segments:
            self.segments = segments
        if self.retail_section:
            self.field_ignore.append('segment')
            self.fields = set(self.fields) - set(self.field_ignore)

    def check_int_float(self, field_name, check_float=False):
        return [item[field_name] for item in self.data \
                    if not(isinstance(item[field_name], int) or isinstance(item[field_name], float))] \
                        if check_float else [item[field_name] for item in self.data \
                            if not isinstance(item[field_name], int)]

    def check_order_field(self):
        result = []
        uniqueness = False if len(set([item['order'] for item in self.data])) != len(self.data) else True
        not_int = [item['order'] for item in self.data if not isinstance(item['order'], int)]
        if not uniqueness:
            result.append({"uniqueness":uniqueness})
        if not_int:
            result.append({"not_int":not_int})
        return result

    def check_keys(self, fields):
        return [ele for item_set in [(set(fields) - set(item.keys())) for item in self.data] for ele in item_set if item_set]

    def is_count_zero_or_not(self, sov_count):
        return any([ True if item.get('total_count') else False for item in sov_count])

    def category_run(self) -> list:
        final_result = {}
        wrong_values = ['', 0, None, 'Nan', False]
        df = pd.DataFrame(self.data)
        df = df.fillna('')
        if self.retail_section:
            try:
                df['segment']
            except KeyError:
                df['segment'] = ''
        final_result['keys_not_found'] = list(set(self.check_keys(fields=self.fields)))

        if not final_result.get('keys_not_found'):
            # processor 
            processor_check = df.loc[(df['processor'] == "amd") & ((df['processor_model'].isin(wrong_values)) | (df['processor_type'].isin(wrong_values)))][['processor_model', 'processor_type', 'link']].to_dict('records')

            processor_type_check = df.loc[(df['processor_type'].isin(['amd', 'athlon', 'ryzen'])) & ((df['processor_model'].isin(wrong_values)) | (df['processor'].isin(wrong_values)))][['processor_model', 'processor', 'link']].to_dict('records')

            final_result['processor'] = [item for item in [processor_check, processor_type_check] if item]

            # Product_name
            final_result['product_name'] = list(df.loc[~(df['product_name'].str.len().isin(range(5, 251)))]['product_name'].values)
            # Price
            # pattern = r"^.?[$-]?[0-9]{1,3}(?:,?[0-9])*(?:\.[0-9]{0,})?$"
            # pattern = r"(^.?[$-円€¥£]?\s?[0-9]{1,3}(?:,?[0-9])*(?:\.[0-9]{0,})?$)|(^.?[0-9]{1,3}(?:,?[0-9])*(?:\.[0-9]{0,})?\s?[$-円€£¥]?$)"
            pattern = r"(^.?[$-円€¥£]?\s?[0-9]{1,3}(?:,?[0-9])*(?:\.[0-9]{0,})?$)|(^.?[0-9]{1,3}(?:,?[0-9])*(?:\.[0-9]{0,})?\s?[$-円€£¥]?$)|(^.?[0-9]{1,3}(?:\.?[0-9])*(?:,[0-9]{0,})?\s?[$-円€£¥]?$)"
            final_result['price'] = list(df.loc[~df['price'].str.contains(pattern, regex=True, na=False)]['price'].values)
            # Offer
            offer = list(df.loc[~df['offer'].str.contains(pattern, regex=True, na=False)]['offer'].values)
            final_result['offer'] = [item for item in offer if not item == '']
            # Image
            final_result['image_count'] = self.check_int_float(field_name='image_count')
            # Link
            final_result['link'] = list(df.loc[~((df['link'].str.len().isin(range(40, 401)) & (df['link'].str.startswith('http'))))]['link'].values)
            # Review
            final_result['reviews'] = self.check_int_float(field_name='reviews')
            # Ratings
            final_result['ratings'] = self.check_int_float(field_name='ratings', check_float=True)
            # Page
            final_result['page'] = self.check_int_float(field_name='page')
            # Page_count
            final_result['page_count'] = self.check_int_float(field_name='page_count')
            # Order
            final_result['order'] = self.check_order_field()
            # Item_category
            item_category = list(df.loc[~df['item_category'].isin(self.categories)]['item_category'].values)
            final_result['item_category'] = {'wrong_category':item_category} if item_category else []
            # Segment
            final_result['segment'] = list(df.loc[~df['segment'].isin(self.segments)]['segment'].values)
            # All Empty values 
            final_result['all_empty_fields'] = [field for field in (set(self.fields) - set(self.field_ignore)) if len(df[field]) == len(df.loc[(df[field].isin(wrong_values))])]

            # Final_result which contains wrong/empty data
            final_result = {k:v for k,v in final_result.items() if v}
            # Ignoring fields
            if self.field_ignore:
                for _field in self.field_ignore:
                    final_result.pop(_field, None)
        return final_result

    def sov_run(self):
        final_result = {}
        wrong_values = ['', 0, None, 'Nan', False]
        df = pd.DataFrame(self.data)
        df = df.fillna('')
        final_result['keys_not_found'] = self.check_keys(fields=self.sov_fields)
        # final_result['total_data'] = len(self.data)

        if not final_result.get('keys_not_found'):
            # Item_category
            item_category = list(df.loc[~df['item_category'].isin(self.categories)]['item_category'].values)
            final_result['item_category'] = {'wrong_category':item_category} if item_category else []
            # Link
            final_result['link'] = list(df.loc[~((df['link'].str.len().isin(range(40, 401)) & (df['link'].str.startswith('http'))))]['link'].values)
            # Product name
            final_result['product_name'] = list(df.loc[~(df['product_name'].str.len().isin(range(5, 251)))]['product_name'].values)
            # All Empty values 
            final_result['all_empty_fields'] = [field for field in (set(self.sov_fields) - set(self.field_ignore)) if len(df[field]) == len(df.loc[(df[field].isin(wrong_values))])]
            # Final_result which contains wrong/empty data
            final_result = {k:v for k,v in final_result.items() if v}
        return final_result

    def run(self):
        if not self.data:
            return yaml.dump({"summary", "Empty data passed, Please verify"}, indent=4, default_flow_style=False)
        result = {}
        if self.category_section or self.retail_section:
            result = self.category_run()
        if self.sov_section:
            result = self.sov_run()
            if not self.is_count_zero_or_not(self.sov_count):
                result['all_count'] = self.is_count_zero_or_not(self.sov_count)
        if self.yaml_dump:
            return yaml.dump(result, indent=4, default_flow_style=False)
        return result


def round2(x, d=0):
    p = 10 ** d
    if x > 0:
        return float(math.floor((x * p) + 0.5))/p
    else:
        return float(math.ceil((x * p) - 0.5))/p



########################## FOR GPU_MODEL GPU GPU_TYPE ###############################
gpu_model_type_map ={
    "3060"  :  [ "nvidia", "nvidia geforce rtx"],
    "580"  :  [ "amd", "amd radeon rx"],
    "6600"  :  [ "amd", "amd radeon rx"],
    "6700xt"  :  [ "amd", "amd radeon rx"],
    "1650"  :  [ "nvidia", "nvidia geforce gtx"],
    "1030"  :  [ "nvidia", "nvidia geforce gt"],
    "6500"  :  [ "amd", "amd radeon rx"],
    "6700"  :  [ "amd", "amd radeon rx"],
    "4080"  :  [ "nvidia", "nvidia geforce rtx"],
    "4070"  :  [ "nvidia", "nvidia geforce rtx"],
    "4090"  :  [ "nvidia", "nvidia geforce rtx"],
    "3070"  :  [ "nvidia", "nvidia geforce rtx"],
    "6950xt"  :  [ "amd", "amd radeon rx"],
    "6650xt"  :  [ "amd", "amd radeon rx"],
    "730"  :  [ "nvidia", "nvidia geforce gt"],
    "1660"  :  [ "nvidia", "nvidia geforce gtx"],
    "7900xt"  :  [ "amd", "amd radeon rx"],
    "3050"  :  [ "nvidia", "nvidia geforce rtx"],
    "3090"  :  [ "nvidia", "nvidia geforce rtx"],
    "6750xt"  :  [ "amd", "amd radeon rx"],
    "7900xtx"  :  [ "amd", "amd radeon rx"],
    "6800"  :  [ "amd", "amd radeon rx"],
    "3080"  :  [ "nvidia", "nvidia geforce rtx"],
    "2060"  :  [ "nvidia", "nvidia geforce rtx"],
    "6400"  :  [ "amd", "amd radeon rx"],
    "710"  :  [ "nvidia", "nvidia geforce gt"]
}

gpu_term_keys = list(gpu_model_type_map.keys())
def squeeze_gpu_info(input_text):
    try:
        input_text = input_text.lower()
        input_text = input_text.replace('-', ' ')
        input_text = input_text.replace('window', ' ').replace('with', ' ').replace('white', ' ')
        input_text= input_text.encode('ascii' , 'ignore').decode()
        match = False
        complete_match = False
        gpu_model , gpu, gpu_type = None, None, None
        for model in gpu_term_keys:
            if model in input_text.split():
                match = True
                complete_match = True
                gpu_model = model
                gpu , gpu_type = gpu_model_type_map[model][0], gpu_model_type_map[model][1]
                break               
        response = {
            'gpu' : '' if not gpu else  gpu.strip() ,
            'gpu_type' : '' if not gpu_type else  gpu_type.strip() ,
            'gpu_model' : '' if not gpu_model else  gpu_model.strip() ,
            'gpu_match' : match,
            'gpu_complete_match' : complete_match,
        }

        return response   
    except Exception as e:
        l.error("Exception in squeeze processor info")
        exc_type, exc_obj, exc_tb  = sys.exc_info()
        l.error( str(exc_type) + ' ---> ' + str(exc_tb.tb_lineno)  +'--->'+ str(exc_obj) )
        l.error('In string --> {}'.format(input_text))
        raise e
