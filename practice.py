from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
opts = Options()
opts.add_argument('--user-agent="{}"'.format(user_agent))
driver = webdriver.Chrome()
driver.get('https://www.hp.com/us-en/shop/pdp/hp-pavilion-laptop-15t-eg100-touch-optional-43f54av-1')
driver.maximize_window()

#First Product Name
p_name = driver.find_element(By.TAG_NAME, 'h1').text
print("Product Name ========== ",p_name)

#Processor Specification of 1st Product
driver.find_element(By.TAG_NAME, 'div[class="accordion-group accordion-1"]').click()

        