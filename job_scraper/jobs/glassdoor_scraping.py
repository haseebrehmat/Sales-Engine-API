from selenium.webdriver.common.by import By
from selenium import webdriver
from job_scraper.constants.const import *
import pandas as pd
import time


class GlassdoorScraping:

    # returns driver
    def driver():
        return webdriver.Chrome()

    def login(driver):
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, "email-input").click()
        driver.find_element(By.ID, "inlineUserEmail").clear()
        driver.find_element(By.ID, "inlineUserEmail").send_keys(GLASSDOOR_USERNAME)
        driver.find_element(By.CLASS_NAME, "email-button").click()

        time.sleep(1)

        driver.find_element(By.CLASS_NAME, "password-input").click()
        driver.find_element(By.ID, "inlineUserPassword").clear()
        driver.find_element(By.ID, "inlineUserPassword").send_keys(GLASSDOOR_PASSWORD)
        driver.find_element(By.CLASS_NAME, "css-1dqhu4c").click()

        login = driver.find_elements(By.CLASS_NAME, "iconContainer")
        if len(login) > 0:
            return False

        time.sleep(5)
        return True

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
        jobs = driver.find_elements(By.CLASS_NAME, "react-job-listing")

        for job in jobs:
            data = []
            job.click()
            time.sleep(3)

            job_title = driver.find_elements(By.CLASS_NAME, "css-1vg6q84")
            if job_title:
                GlassdoorScraping.append_data(data, job_title[0].text)
                c_name = driver.find_element(By.CLASS_NAME, "css-87uc0g")
                company_name = c_name.text.split("\n")
                GlassdoorScraping.append_data(data, company_name[0])
                address = driver.find_element(By.CLASS_NAME, "css-56kyx5")
                GlassdoorScraping.append_data(data, address.text)
                job_description = driver.find_element(By.CLASS_NAME, "jobDescriptionContent")
                GlassdoorScraping.append_data(data, job_description.text)
                url = driver.find_elements(By.CLASS_NAME, "css-1rd3saf")
                GlassdoorScraping.append_data(data, url[count].get_attribute('href'))
                job_posted_date = driver.find_elements(By.CLASS_NAME, "css-1vfumx3")
                GlassdoorScraping.append_data(data, job_posted_date[count].text)
                GlassdoorScraping.append_data(data, "Glassdoor")
                GlassdoorScraping.append_data(data, job_type)

            scrapped_data.append(data)
            count += 1

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                        "job_source", "job_type"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        df.to_csv(GLASSDOOR_CSV, index=False)

        if not GlassdoorScraping.data_exists(driver):
            return False

        next_page = driver.find_element(By.CLASS_NAME, "nextButton")
        next_page.click()

        return True

    # check if there is more jobs available or not
    def data_exists(driver):
        pagination = driver.find_element(By.CLASS_NAME, "nextButton")
        next_page = pagination.get_attribute('disabled')
        return False if next_page else True


# code starts from here
def glassdoor():
    scrapped_data = []
    count = 0
    scrap = GlassdoorScraping
    driver = scrap.driver()
    scrap.request_url(driver, GLASSDOOR_LOGIN_URL)
    logged_in = scrap.login(driver)
    types = [GLASSDOOR_CONTRACT_RESULTS, GLASSDOOR_FULL_RESULTS, GLASSDOOR_REMOTE_RESULTS]
    job_type = ["Contract", "Full Time on Site", "Full Time Remote"]
    if logged_in:
        for url in types:
            scrap.request_url(driver, url)
            while scrap.find_jobs(driver, scrapped_data, job_type[count]):
                print("Fetching...")
            count = count + 1
            print(SCRAPING_ENDED)
