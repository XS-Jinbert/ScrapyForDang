import selenium
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.washingtonpost.com/newssearch/?datefilter=60%20Days&query=china%20threat%20&sort=Relevance&startat=0#top')