from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time

REGIONS = [
   'ljubljana-mesto',
   'ljubljana-okolica',
   'juzna-primorska',
   'severna-primorska',
   'notranjska'
]

def get_items(browser, type):
    f = open('{type}.json')
    old = json.load(f)

    wait = WebDriverWait(browser, 10)

    url = 'https://www.nepremicnine.net/oglasi-prodaja/{REGIONS[r]}/{type}?s=16'
    if type == "posest":
        url = 'https://www.nepremicnine.net/oglasi-prodaja/{REGIONS[r]}/{type}/zazidljiva?s=16'
    
    browser.get(url)
    element_list = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title > a"))
    )
    for element in element_list:
        try:
            title, url = element.text, element.get_attribute('href')
            print("Title:", title, "\nURL:", url, end="\n\n")
        except Exception as e:
            print(e)

def scrape():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    get_items(browser, "posest")

    time.sleep(2)
    browser.quit()

if __name__ == '__main__':
    print("Starting scrape...")
    scrape()