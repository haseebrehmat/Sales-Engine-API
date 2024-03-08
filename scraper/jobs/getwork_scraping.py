import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs

total_job = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type):
    try:
        c = 0
        scrapped_data = []
        time.sleep(2)
        job_links = []
        links = driver.find_elements(By.CLASS_NAME, "job-listing")
        if len(links) == 0:
            return False
        for link in links:
            job_links.append(link.get_attribute('data-job-url'))
        original_window = driver.current_window_handle
        for job in job_links:
            try:
                data = []
                job_details = links[c].text.split("\n")
                append_data(data, job_details[0])
                append_data(data, job_details[1])
                append_data(data, job_details[2])
                append_data(data, job_details[4])
                driver.switch_to.new_window('tab')
                driver.get('https://getwork.com' + str(job))
                job_description = driver.find_element(By.CLASS_NAME, "job-description")
                append_data(data, job_description.text)
                append_data(data, driver.current_url)
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "GetWork")
                append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))

                scrapped_data.append(data)
            except Exception as e:
                print(e)
            c += 1
            driver.close()
            driver.switch_to.window(original_window)

        columns_name = ["job_title", "company_name", "address",  "job_posted_date", "job_description", "job_source_url", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.GETWORK)
        df.to_excel(filename, index=False)

        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="GetWork", filename=filename)

        pagination = driver.find_element(By.CLASS_NAME, "job-listing-pagination")
        pagination.location_once_scrolled_into_view
        btn = pagination.find_elements(By.TAG_NAME, "a")
        btn[-1].click()
        return True
    except Exception as e:
        saveLogs(e)
        print(e)
        return False


# code starts from here
def getwork(link, job_type):
    print("Getwork")
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, link)
            while flag:
                flag = find_jobs(driver, job_type)
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)
    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()
