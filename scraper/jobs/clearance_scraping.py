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
        links = driver.find_elements(By.CLASS_NAME, "job-search-list-item-desktop__job-name")
        for link in links:
                job_links.append(link.get_attribute('href'))
        original_window = driver.current_window_handle
        for job in job_links:
            try:
                data = []
                driver.switch_to.new_window('tab')
                driver.get(job)
                time.sleep(4)
                job_title = driver.find_element(By.CLASS_NAME, "job-name")
                append_data(data, job_title.text.replace('- job post', ''))
                company_name = driver.find_element(By.CLASS_NAME, "job-location")
                append_data(data, company_name.text)
                address = driver.find_element(By.CLASS_NAME, "job-view__location-name")
                append_data(data, address.text)
                job_description = driver.find_element(By.CLASS_NAME, "job-description-text")
                append_data(data, job_description.text)
                append_data(data, driver.current_url)
                job_posted_date = driver.find_element(By.CLASS_NAME, "job-info-item")
                append_data(data, job_posted_date.text)
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "Clearance")
                append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))

                scrapped_data.append(data)
                c += 1
                total_job += 1
                driver.close()
                driver.switch_to.window(original_window)
            except Exception as e:
                print(e)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.CLEARANCE)
        df.to_excel(filename, index=False)

        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Clearance", filename=filename)

        next_page = driver.find_element(By.CLASS_NAME, "btn--next")
        next_page.location_once_scrolled_into_view
        if next_page.get_attribute('disabled') == 'true':
            return False, total_job
        next_page.click()
        return True, total_job
    except Exception as e:
        saveLogs(e)
        return False, total_job


# code starts from here
def clearance(link, job_type):
    print("Clearance")
    driver = configure_webdriver()
    try:
        total_job = 0
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, link)
            driver.maximize_window()
            while flag:
                flag, total_job = find_jobs(
                    driver, job_type, total_job)
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)
    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()
