from typing import List, Union
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#For tags
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import BaseOptions
#For wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

webdriver_url = 'http://localhost:4444/wd/hub'

firefox_options = webdriver.FirefoxOptions()
chrome_options=webdriver.ChromeOptions()
edge_options = webdriver.EdgeOptions()

driver = webdriver.Remote(webdriver_url, options=edge_options)

driver.get('https://id-panel-stage.agros.tech/')
print(type(driver.page_source))