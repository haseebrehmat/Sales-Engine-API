import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from scraper.constants.const import *
from scraper.models import ScraperLogs
# from selenium.webdriver.support.ui import WebDriverWait
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
    try:
        jobs = driver.find_elements(By.CLASS_NAME, "gc-card")

        address = driver.find_elements(By.CLASS_NAME, "gc-job-tags__location")

        for job in jobs[:-1]:
            data = []
            try:
                job.location_once_scrolled_into_view
                job.click()
            except Exception as e:
                print(e)

            time.sleep(2)
            job_title = driver.find_elements(By.CLASS_NAME, "gc-card__title")
            append_data(data, job_title[count].text)
            company_name = driver.find_elements(By.CLASS_NAME, "gc-job-tags__team")
            append_data(data, company_name[0].text)
            try:
                append_data(data, address[count].text.split('\n')[1])
            except Exception as e:
                append_data(data, address[count].text.split('\n')[0])
            job_description = driver.find_elements(By.CLASS_NAME, "gc-card__content")
            append_data(data, job_description[0].text)
            append_data(data, job.get_attribute('href'))
            # job_posted_date = driver.find_elements(By.CLASS_NAME,"posted-date")
            append_data(data, "Today")
            append_data(data, "Google Careers")
            append_data(data, job_type)
            append_data(data, job_description[0].get_attribute('innerHTML'))

            count += 1
            total_job += 1
            scrapped_data.append(data)

        date_time = str(datetime.now())
        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                        "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = f'scraper/job_data/googlecareers - {date_time}.xlsx'
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(df), job_source="GoogleCareers", filename=filename)

        cookie = driver.find_elements(By.CLASS_NAME, "gc-cookie-bar__buttons")
        if len(cookie) > 0:
            c_button = cookie[0].find_elements(
                By.CLASS_NAME, "gc-button--raised")
            c_button[0].click()

    except Exception as e:
        print(e)

    time.sleep(2)
    next_page = driver.find_elements(By.CLASS_NAME, "gc-link--on-grey")
    try:
      next_page[1].location_once_scrolled_into_view
      next_page[1].click()
      time.sleep(2)
      return True, total_job
    except Exception as e:
      print(e)
    return False, total_job

def job_display(driver):
    time.sleep(3)
    expand = driver.find_elements(By.CLASS_NAME, "gc-card__cta")
    try:
        expand[0].click()
        time.sleep(3)
        return True, total_job
    except Exception as e:
        saveLogs(e)
        print("No jobs to display")
        return False, total_job

# code starts from here
def google_careers(links, job_type):
    print("Google Careers")
    total_job = 0
    options = webdriver.ChromeOptions()  # newly added
    options.add_argument("--headless")
    options.add_argument("window-size=1200,1100")
    options.add_argument('--log-level=0')  # Set the log level to ALL
    options.add_argument('--disable-logging')  # Disable logging to the console
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    )
    # options.headless = True  # newly added
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                          options=options) as driver:  # modified
        # driver = webdriver.Chrome('/home/dev/Desktop/selenium')
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, links)
            if job_display(driver):
                while flag:
                    flag, total_job = find_jobs(driver, job_type, total_job)
                    print("Fetching...")
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print("Failed")
        driver.quit()
