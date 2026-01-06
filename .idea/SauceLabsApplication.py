from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import  Options
import time
from selenium.webdriver.support.ui import WebDriverWait #wait import
from selenium.webdriver.support import expected_conditions as EC #explicit wait
from selenium.webdriver.common.keys import Keys #import keys

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service('/Users/sumana/Downloads/chromedriver-mac-arm64 2/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://sauce-demo.myshopify.com/account/login')

time.sleep(5)

UserName= "//input[@id='idToken1']"

EC.visibility_of_element_located(UserName);
driver.find_element(By.XPATH,UserName).clear()
driver.find_element(By.XPATH,UserName).send_keys()
