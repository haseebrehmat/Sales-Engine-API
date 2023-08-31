import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver
from utils.helpers import saveLogs

total_job = 0


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
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "card-title-link"))
    )
    jobs = driver.find_elements(By.TAG_NAME, "dhi-search-card")

    job_title = driver.find_elements(By.CLASS_NAME, "card-title-link")
    for job in jobs:
        try:
            data = []
            append_data(data, job_title[count].text)
            c_name = driver.find_elements(By.CLASS_NAME, "card-company")
            company_name = c_name[count].find_elements(By.TAG_NAME, "a")
            for company in company_name:
                append_data(data, company.text)
            address = driver.find_elements(By.CLASS_NAME, "search-result-location")
            append_data(data, address[count].text)
            job_url = job_title[count].get_attribute('href')
            original_window = driver.current_window_handle
            driver.switch_to.new_window('tab')
            driver.get(job_url)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "job-description")))
            job_description = driver.find_element(By.CLASS_NAME, "job-description")
            append_data(data, job_description.text)
            append_data(data, job_url)
            job_posted_date = driver.find_element(By.CLASS_NAME, "sc-dhi-time-ago")
            append_data(data, job_posted_date.text.split(" |")[0])
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "Dice")
            append_data(data, job_type)
            append_data(data, job_description.get_attribute('innerHTML'))
            count += 1
            total_job += 1
            scrapped_data.append(data)
            driver.close()
            driver.switch_to.window(original_window)
            time.sleep(0.5)
        except Exception as e:
            print(e)
        time.sleep(1)

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.DICE)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(total_jobs=len(df), job_source="Dice", filename=filename)

    finished = "disabled"
    pagination = driver.find_elements(By.CLASS_NAME, "pagination-next")
    try:
        next_page = pagination[0].get_attribute('class')
        if finished in next_page:
            return False, total_job
        else:
            pagination[0].click()
            time.sleep(5)
        return True, total_job
    except Exception as e:
        print(e)
        return False, total_job


# code starts from here
def dice(link, job_type):
    total_job = 0
    print("Dice")
    try:
        driver = configure_webdriver()
        driver.maximize_window()
        flag = True
        try:
            request_url(driver, link)
            while flag:
                flag, total_job = find_jobs(driver, job_type, total_job)
                print("Fetching...")
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)

        driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)
