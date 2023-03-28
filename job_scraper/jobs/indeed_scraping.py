from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from job_scraper.constants.const import *
from selenium import webdriver

import pandas as pd
import time


class IndeedScraping:

    # returns driver
    def driver():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(chrome_options=chrome_options)

    # calls url
    def request_url(driver, url):
        driver.get(url)

    # driver wait after login to complete it's verification process
    def driver_wait():
        time.sleep(3)
        time.sleep(3)

    # append data for csv file
    def append_data(data, field):
        data.append(str(field).strip("+"))

    # find's job name
    def find_jobs(driver, scrapped_data, job_type):
        time.sleep(3)
        jobs = driver.find_elements(By.CLASS_NAME, "slider_container")

        for job in jobs:
            data = []
            time.sleep(1)
            job.click()
            time.sleep(3)

            job_title = driver.find_element(By.CLASS_NAME, "jobsearch-JobInfoHeader-title")
            IndeedScraping.append_data(data, job_title.text.replace('- job post', ''))
            c_name = driver.find_elements(By.CLASS_NAME, "css-1cjkto6")
            company_name = c_name[1].find_elements(By.TAG_NAME, "a")
            for company in company_name:
                IndeedScraping.append_data(data, company.text)
            address = driver.find_element(By.CLASS_NAME, "css-6z8o9s")
            IndeedScraping.append_data(data, address.text.replace('•Remote', ''))
            job_description = driver.find_element(By.CLASS_NAME, "jobsearch-jobDescriptionText")
            IndeedScraping.append_data(data, job_description.text)
            IndeedScraping.append_data(data, driver.current_url)
            job_posted_date = driver.find_elements(By.CLASS_NAME, "css-5vsc1i")
            IndeedScraping.append_data(data, job_posted_date[0].text)
            IndeedScraping.append_data(data, "Indeed")
            IndeedScraping.append_data(data, job_type)

            scrapped_data.append(data)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                        "job_source", "job_type"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        df.to_csv(INDEED_CSV)

        if not IndeedScraping.data_exists(driver):
            return False

        next_page = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next Page']")
        next_page.click()

        return True

    # check if there is more jobs available or not
    def data_exists(driver):
        page_exists = driver.find_elements(By.CSS_SELECTOR, "a[aria-label='Next Page']")
        return False if len(page_exists) == 0 else True


# code starts from here
def indeed():
    count = 0
    scrap = IndeedScraping
    driver = scrap.driver()
    driver.maximize_window()
    types = [INDEED_CONTRACT_RESULTS, INDEED_FULL_RESULTS, INDEED_REMOTE_RESULTS]
    job_type = ["Contract", "Full Time on Site", "Full Time Remote"]
    for url in types:
        scrapped_data = []
        scrap.request_url(driver, url)
        while scrap.find_jobs(driver, scrapped_data, job_type[count]):
            print("Fetching...")
        count = count + 1
    print(SCRAPING_ENDED)
