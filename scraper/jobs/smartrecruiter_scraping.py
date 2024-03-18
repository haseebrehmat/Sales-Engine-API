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
def find_jobs(driver, job_type, total_job):
    try:
        c = 0
        scrapped_data = []
        time.sleep(3)
        job_links = []
        links = driver.find_elements(By.CLASS_NAME, "job")
        for link in links:
                job_links.append(link.get_attribute('href'))
        job_details = driver.find_elements(By.CLASS_NAME, "job-details")

        original_window = driver.current_window_handle
        for job in job_links:
            try:
                data = []
                job_detail = job_details[c].find_elements(By.TAG_NAME, "li")
                append_data(data, job_detail[0].text)
                append_data(data, job_detail[1].text)
                driver.switch_to.new_window('tab')
                driver.get(job)
                job_title = driver.find_element(By.CLASS_NAME, "job-title")
                append_data(data, job_title.text)
                loc = driver.find_element(By.CLASS_NAME, "job-details")
                address = loc.find_element(By.TAG_NAME, "li")
                append_data(data, address.text)
                job_description = driver.find_element(By.CLASS_NAME, "job-sections")
                append_data(data, job_description.text)
                append_data(data, driver.current_url)
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "Smart Recruiter")
                job_type_check = driver.find_element(By.CLASS_NAME, "job-details").text.lower()
                if 'contract' in job_type_check:
                    append_data(data, set_job_type('contract'))
                elif 'full-time' in job_type_check:
                    append_data(data, set_job_type('full time'))
                else:
                    append_data(data, set_job_type('full time'))
                append_data(data, job_description.get_attribute('innerHTML'))

                scrapped_data.append(data)
                c += 1
                total_job += 1
                driver.close()
                driver.switch_to.window(original_window)
            except Exception as e:
                print(e)

        columns_name = ["company_name", "job_posted_date", "job_title", "address", "job_description", "job_source_url", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.SMARTRECRUITER)
        df.to_excel(filename, index=False)

        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Smart Recruiter", filename=filename)
    except Exception as e:
        saveLogs(e)


# code starts from here
def smartrecruiter(link, job_type):
    print("Smart Recruiter")
    driver = configure_webdriver()
    try:
        total_job = 0
        driver.maximize_window()
        try:
            request_url(driver, link)
            driver.maximize_window()
            find_jobs(driver, job_type, total_job)
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)
    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()
