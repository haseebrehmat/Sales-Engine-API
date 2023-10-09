import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from utils.helpers import saveLogs
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type

total_job = 0

def check_alerts(driver):
    time.sleep(2)
    try:
        if driver.find_element(By.CLASS_NAME, "js-join-community"):
            driver.find_element(By.CLASS_NAME, "js-email-join").click()
            driver.find_element(By.CLASS_NAME, "js-email-join").clear()
            driver.find_element(By.CLASS_NAME, "js-email-join").send_keys("m.abubakartariq@devsinc.com")
            driver.find_element(By.CLASS_NAME, "js-join-community").click()
    except:
        pass


def file_creation(scrapped_data):
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                    "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.DAILY_REMOTE)

    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Daily Remote", filename=filename)


def find_jobs(driver, job_type, total_job):
    count = 0
    check_alerts(driver)
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    time.sleep(1)
    details_window = driver.current_window_handle
    driver.switch_to.window(original_window)
    flag_count = 1
    page_count = 1
    while(flag_count <= int(page_count)):
        driver.switch_to.window(original_window)
        check_alerts(driver)
        complete_div = driver.find_elements(By.CLASS_NAME, "card-container")
        time.sleep(2)
        jobs = complete_div[0].find_elements(By.TAG_NAME, "article")
        try:
            for job in jobs:
                job.location_once_scrolled_into_view
        except:
            pass
        scrapped_data = []
        for job in jobs:
            data = []
            try:
                driver.switch_to.window(original_window)
                check_alerts(driver)
                job_link = job.find_elements(By.TAG_NAME, "a")[0].get_attribute('href')
                driver.switch_to.window(details_window)
                driver.get(job_link)
                time.sleep(3)
                job_title = driver.find_elements(By.CLASS_NAME, "profile-information")[0].text
                job_description = driver.find_elements(By.CLASS_NAME, "job-full-description")
                company_name = driver.find_elements(By.CLASS_NAME, "company-info-block")[0]
                company_name = company_name.find_elements(By.CLASS_NAME, "company-name")[0].text
                job_posted_date = driver.find_elements(By.CLASS_NAME, "meta-holder")[0].text
                location = driver.find_elements(By.CLASS_NAME, "meta-holder")[1].text
                job_type = job_type
                job_source = "dailyremote"
                job_source_url = job_link
                append_data(data, job_title)
                append_data(data, company_name)
                append_data(data, location)
                append_data(data, job_description[0].text)
                append_data(data, job_source_url)
                append_data(data, job_posted_date)
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, job_source)
                append_data(data, set_job_type(job_type))
                append_data(data, job_description[0].get_attribute('innerHTML'))
                total_job += 1
                scrapped_data.append(data)
            except Exception as e:
                print(e)
        # Here is a file uploading code
        file_creation(scrapped_data)
        from scraper.schedulers.job_upload_scheduler import upload_jobs, remove_files
        upload_jobs('instant scraper', job_source)
        remove_files('instant scraper', job_source)
        scrapped_data = []
        try:
            driver.switch_to.window(original_window)
            page_count = int(driver.find_elements(By.CLASS_NAME, "pagination-page")[-2].text)
            next_page_link = driver.find_elements(By.CLASS_NAME, "pagination-page")[-1].get_attribute('href')
            driver.get(next_page_link)
            time.sleep(3)
            flag_count += flag_count
        except:
            flag_count += flag_count
    return False, total_job


def append_data(data, field):
    data.append(str(field).strip("+"))


# Create your views here.
def dailyremote(link, job_type):
    print("Daily Remote")
    try:
        total_job = 0
        driver = configure_webdriver()
        driver.maximize_window()
        try:
            flag = True
            driver.get(link)
            while flag:
                flag, total_job = find_jobs(
                    driver, job_type, total_job)
                print("Fetching...")
        except Exception as e:
            print(e)
        driver.quit()
    except:
        print("Error Occurs. \n")
