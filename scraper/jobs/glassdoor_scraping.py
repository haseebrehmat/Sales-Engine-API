import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming
from utils.helpers import saveLogs

total_job = 0


def login(driver):
    try:
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "email-input").click()
        driver.find_element(By.ID, "inlineUserEmail").clear()
        driver.find_element(By.ID, "inlineUserEmail").send_keys(
            GLASSDOOR_USERNAME)
        driver.find_element(By.CLASS_NAME, "email-button").click()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "password-input").click()
        driver.find_element(By.ID, "inlineUserPassword").clear()
        driver.find_element(By.ID, "inlineUserPassword").send_keys(
            GLASSDOOR_PASSWORD)
        driver.find_element(By.CLASS_NAME, "css-jbcabp").click()
        login = driver.find_elements(By.CLASS_NAME, "iconContainer")
        if len(login) > 0:
            return False
        time.sleep(5)
        return True
    except Exception as e:
        print(e)
        return False


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    count = 0
    time.sleep(3)
    date_time = str(datetime.now())
    try:
        jobs = driver.find_elements(By.CLASS_NAME, "react-job-listing")
        for job in jobs:
            try:
                data = []
                job.click()
                time.sleep(2)
                job_title = driver.find_elements(By.CLASS_NAME, "css-1vg6q84")
                company_name = driver.find_element(
                    By.CLASS_NAME, "e1tk4kwz1")
                if job_title:
                    append_data(data, job_title[0].text)
                    append_data(data, company_name.text)
                    address = driver.find_element(By.CLASS_NAME, "css-56kyx5")
                    append_data(data, address.text)
                    job_description = driver.find_element(
                        By.CLASS_NAME, "jobDescriptionContent")
                    append_data(data, job_description.text)
                    url = driver.find_elements(By.CLASS_NAME, "jobCard")
                    append_data(data, url[count].get_attribute('href'))
                    try:
                        job_posted_date = driver.find_elements(
                            By.CLASS_NAME, "listing-age")
                        append_data(data, job_posted_date[count].text)
                    except Exception as e:
                        print(e)
                        append_data(data, "24h")
                    append_data(data, "Glassdoor")
                    append_data(data, job_type)
                    append_data(data, job_description.get_attribute('innerHTML'))
                scrapped_data.append(data)
                count += 1
                total_job += 1
            except Exception as e:
                print(e)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                        "job_source", "job_type", "job_description_tags"]
        filename = generate_scraper_filename(ScraperNaming.GLASSDOOR)
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="GlassDoor", filename=filename)
    except Exception as e:
        saveLogs(e)
        print(e)

    try:
        if driver.find_element(By.CLASS_NAME, "nextButton").is_enabled():
            driver.find_element(By.CLASS_NAME, "nextButton").click()
            return True, total_job
        return False, total_job
    except Exception as e:
        print(e)
        return False, total_job


# code starts from here
def glassdoor(link, job_type):
    print("Glassdoor")
    try:
        total_job = 0
        count = 0
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options) as driver:  # modified
            request_url(driver, GLASSDOOR_LOGIN_URL)
            driver.maximize_window()
            logged_in = login(driver)
            try:
                if logged_in:
                    flag = True
                    request_url(driver, link)
                    while flag:
                        flag, total_job = find_jobs(
                            driver, job_type, total_job)
                        count += 1
                    print(SCRAPING_ENDED)
            except Exception as e:
                saveLogs(e)
                print(LINK_ISSUE)

            driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)
