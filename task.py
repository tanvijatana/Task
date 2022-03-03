from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# driver = webdriver.Chrome()
driver = webdriver.Chrome()
driver.get('https://www.hp.com/us-en/shop/vwa/laptops/segm=Home?jumpid=ma_lt_featured_na_6_210303')
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Getting Product Link
prod_link = soup.select_one("[id = 'p_3074457345620102824'] a")['href']
driver.get("https://www.hp.com"+prod_link)
driver.maximize_window()

#First Product Name
p_name = driver.find_element(By.TAG_NAME, 'h1').text
print("Product Name ========== ",p_name)

#Processor Specification of 1st Product
time.sleep(3)
driver.find_element(by=By.CSS_SELECTOR, value='li[aria-label="Specs"]').click()
time.sleep(2)

for spec in driver.find_elements(by=By.CSS_SELECTOR, value='div[class="specs-row clearfix"]'):
    if spec.find_element(by=By.CSS_SELECTOR, value='h2').text == "Processor and graphics":
        print("Processor and Graphics Specification ==========",spec.find_element(by=By.CSS_SELECTOR, value='div[class="spec-value"]').text)


        