from datetime import datetime

from job_scraper.constants.const import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, scrapped_data, job_type):
    date_time = str(datetime.now())
    count = 0
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "card-title-link"))
    )
    jobs = driver.find_elements(By.TAG_NAME, "dhi-search-card")

    for job in jobs:
        data = []

        job_title = driver.find_elements(By.CLASS_NAME, "card-title-link")
        append_data(data, job_title[count].text)
        c_name = driver.find_elements(By.CLASS_NAME, "card-company")
        company_name = c_name[count].find_elements(By.TAG_NAME, "a")
        for company in company_name:
            append_data(data, company.text)
        address = driver.find_elements(By.CLASS_NAME, "search-result-location")
        append_data(data, address[count].text)
        job_description = driver.find_elements(By.CLASS_NAME, "card-description")
        append_data(data, job_description[count].text)
        append_data(data, driver.current_url)
        job_posted_date = driver.find_elements(By.CLASS_NAME, "posted-date")
        append_data(data, job_posted_date[count].text)
        append_data(data, "Dice")
        append_data(data, job_type)

        count += 1
        scrapped_data.append(data)

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "job_source", "job_type"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(f"job_scraper/job_data/dice_results - {date_time}.csv", index=False)

    finished = "disabled"
    pagination = driver.find_elements(By.CLASS_NAME, "pagination-next")
    next_page = pagination[0].get_attribute('class')
    if finished in next_page:
        return False
    else:
        pagination[0].click()
        time.sleep(5)

    return True


# code starts from here
def dice():
    count = 0
    scrapped_data = []
    options = webdriver.ChromeOptions()  # newly added
    options.add_argument("--headless")
    options.add_argument("window-size=1200,1100")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    )
    # options.headless = True  # newly added
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                          options=options) as driver:  # modified
        types = [DICE_CONTRACT_RESULTS, DICE_FULL_RESULTS, DICE_REMOTE_RESULTS]
        job_type = ["Contract", "Full Time on Site", "Full Time Remote"]
        for url in types:
            request_url(driver, url)
            while find_jobs(driver, scrapped_data, job_type[count]):
                print("Fetching...")
            count = count + 1
    print(SCRAPING_ENDED)
