from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from job_scraper.constants.const import *
import pandas as pd
import time


class SimplyHiredScraping:

    # returns driver
    def driver():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(chrome_options=chrome_options)

    # calls url
    def request_url(driver, url):
        driver.get(url)

    # append data for csv file
    def append_data(data, field):
        data.append(str(field).strip("+"))

    # find's job name
    def find_jobs(driver, scrapped_data, job_type):
        count = 0
        time.sleep(3)
        jobs = driver.find_elements(By.CLASS_NAME, "css-12bkbc3")

        for job in jobs:
            data = []
            job.click()
            time.sleep(5)

            job_title = driver.find_element(By.CLASS_NAME, "chakra-heading")
            SimplyHiredScraping.append_data(data, job_title.text)
            context = driver.find_elements(By.CLASS_NAME, "css-xtodu4")
            company_name = context[0].text.split("-")
            SimplyHiredScraping.append_data(data, company_name[0])
            address = context[1].text
            SimplyHiredScraping.append_data(data, address)
            job_description = driver.find_element(By.CLASS_NAME, "css-imewub")
            SimplyHiredScraping.append_data(data, job_description.text)
            SimplyHiredScraping.append_data(data, job.get_attribute('href'))
            job_posted_date = context[4].text
            SimplyHiredScraping.append_data(data, job_posted_date)
            SimplyHiredScraping.append_data(data, "Simply Hired")
            SimplyHiredScraping.append_data(data, job_type)

            scrapped_data.append(data)
            count += 1

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                        "job_source", "job_type"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        df.to_csv(SIMPLYHIREDCSV)

        if not SimplyHiredScraping.data_exists(driver):
            return False

        next_page = driver.find_element(By.CLASS_NAME, "css-gxlopd")
        next_page.click()

        return True

    # check if there is more jobs available or not
    def data_exists(driver):
        pagination = driver.find_elements(By.CLASS_NAME, "css-gxlopd")
        return False if len(pagination) == 0 else True


# code starts from here
def simply_hired():
    count = 0
    scrapped_data = []
    scrap = SimplyHiredScraping
    driver = scrap.driver()
    types = [SIMPLYHIREDCONTRACT, SIMPLYHIREDFULL, SIMPLYHIREDREMOTE]
    job_type = ["Contract", "Full Time on Site", "Full Time Remote"]
    for url in types:
        scrapped_data = []
        scrap.request_url(driver, url)
        while scrap.find_jobs(driver, scrapped_data, job_type[count]):
            print("Fetching...")
        count = count + 1
    print(SCRAPING_ENDED)


simply_hired()
