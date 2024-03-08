import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type
from utils.helpers import saveLogs

total_job = 0

def hide_alerts(driver):
    try:
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'hide-control')))
        driver.find_element(By.CLASS_NAME, 'hide-control').click()
    except Exception as e:
        print(e)
    time.sleep(2)
    try:
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'close-modal')))
        driver.find_element(By.CLASS_NAME, 'close-modal').click()
    except Exception as e:
        print(e)
    time.sleep(2)
    try:
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.ID, 'job-notification')))
        driver.find_element(By.ID, 'job-notification').find_element(By.CLASS_NAME, 'close').click()
    except Exception as e:
        print(e)
    time.sleep(2)

def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    count = 0
    try:
        hide_alerts(driver)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "result-item")))
        time.sleep(3)
        jobs = driver.find_elements(By.CLASS_NAME, "result-item")
        if jobs:
            jobs[0].click()
        try:
            for job in jobs:
                job.location_once_scrolled_into_view
        except Exception as e:
            print(e)
        time.sleep(3)
        jobs = driver.find_elements(By.CLASS_NAME, "result-item")
        for job in jobs:
            data = []
            try:
                job_title = job.find_elements(By.CLASS_NAME, "title")[0].text
                job_description = job.find_elements(By.CLASS_NAME, "description_short")[0].text
                company_name = job.find_elements(By.CLASS_NAME, "site")[0].text.split(' (')[0]
                job_posted_date = job.find_elements(By.CLASS_NAME, "date")[0].text
                location = job.find_elements(By.CLASS_NAME, "site")[0].text.split(' (')[1][:-1].strip()
                job_type = job_type
                job_source = "recruit"
                job_source_url = job.find_elements(By.CLASS_NAME, "title")[0].find_element(By.TAG_NAME, 'a').get_attribute(
                    'href')
                append_data(data, job_title)
                append_data(data, company_name)
                append_data(data, location)
                append_data(data, job_description)
                append_data(data, job_source_url)
                append_data(data, job_posted_date)
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, job_source)
                append_data(data, set_job_type(job_type))
                append_data(data, 'N/A')
                total_job += 1
                scrapped_data.append(data)
            except Exception as e:
                print(e)
                saveLogs(e)
            count += 1
    except Exception as e:
        saveLogs(e)

    update_job_description(driver, scrapped_data)
    hide_alerts(driver)
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                    "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)

    filename = generate_scraper_filename(ScraperNaming.RECRUIT)

    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(total_jobs=len(df), job_source="Recruit", filename=filename)
    try:
        pagination = driver.find_elements(By.CLASS_NAME, "paging")[0].find_elements(By.TAG_NAME, 'li')
        index = pagination[-1].get_attribute('class').find('disabled')
        if not pagination or index != -1:
            return False
        else:
            pagination[-1].click()
            hide_alerts(driver)
            return True
    except Exception as e:
        saveLogs(e)
        return False


def update_job_description(driver, data):
    current_url = driver.current_url
    try:
        for i in range(len(data)):
            driver.get(data[i][4])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jd-des")))
            job_description = driver.find_element(By.CLASS_NAME, "jd-des")
            data[i][3] = job_description.text
            data[i][-1] = job_description.get_attribute('innerHTML')
    except Exception as e:
        saveLogs(e)
    driver.get(current_url)

def append_data(data, field):
    data.append(str(field).strip("+"))


# Create your views here.
def recruit(link, job_type):
    print("Recruit")
    driver = configure_webdriver()
    try:
        total_job = 0
        driver.maximize_window()
        try:
            flag = True
            driver.get(link)
            while flag:
                flag = find_jobs(driver, job_type, total_job)
                print("Fetching...")
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
    driver.quit()
