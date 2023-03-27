from selenium.webdriver.common.by import By
from job_scraper.constants.const import *
from selenium import webdriver
import pandas as pd
import time


class CareerBuilderScraping:

    # returns driver
    def driver():
        return webdriver.Chrome(executable_path='chromedriver.exe')

    # calls url
    def request_url(driver, url):
        driver.get(url)

    # append data for csv file
    def append_data(data, field):
        data.append(str(field).strip("+"))

    # check if there is more jobs available or not
    def data_exists(driver):
        finished = "display: none;"
        page_exists = driver.find_element(By.CLASS_NAME, "btn-clear-blue")
        display = page_exists.get_attribute('style')
        return False if finished in display else True

    def find_jobs(driver, scrapped_data):
        count = 0
        jobs = driver.find_elements(By.CLASS_NAME, "data-results-content-parent")

        for job in jobs:
            print(count)
            data = []
            time.sleep(1)
            job.click()
            time.sleep(3)

            job_title = driver.find_element(By.CLASS_NAME, "jdp_title_header")
            CareerBuilderScraping.append_data(data, job_title.text)
            c_name = driver.find_elements(By.CLASS_NAME, "data-display-header_info-content")
            company = c_name[0].find_elements(By.TAG_NAME, "span")
            CareerBuilderScraping.append_data(data, company[0].text)
            CareerBuilderScraping.append_data(data, company[1].text)
            job_description = driver.find_element(By.CLASS_NAME, "jdp-left-content")
            CareerBuilderScraping.append_data(data, job_description.text)
            CareerBuilderScraping.append_data(data, driver.current_url)
            job_posted_date = driver.find_elements(By.CLASS_NAME, "data-results-publish-time")
            CareerBuilderScraping.append_data(data, job_posted_date[count].text)

            scrapped_data.append(data)
            count += 1

    # find's job name
    def load_jobs(driver):
        time.sleep(2)

        if not CareerBuilderScraping.data_exists(driver):
            return False

        next_page = driver.find_element(By.CLASS_NAME, "btn-clear-blue")
        next_page.click()
        time.sleep(3)

        return True


# code starts from here
def career_builder():
    scrapped_data = []
    scrap = CareerBuilderScraping
    driver = scrap.driver()
    driver.maximize_window()
    scrap.request_url(driver, CAREERBUILDER_CONTRACT_RESULTS)
    while scrap.load_jobs(driver):
        print("Fetching...")

    scrap.find_jobs(driver, scrapped_data)

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(CAREER_BUILDER_CSV)
