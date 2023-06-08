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

total_job = 0


def find_jobs(driver, scrapped_data, job_type, total_job):
    date_time = str(datetime.now())
    count = 0
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "yKsady"))
    )
    time.sleep(3)
    alert = driver.find_elements(By.CLASS_NAME, "osfoL0")
    if len(alert) > 0:
        alert[0].click()
    jobs = driver.find_elements(By.CLASS_NAME, "yKsady")
    try:
        for job in jobs:
            job.location_once_scrolled_into_view
    except:
        print("Do not load the whole page")
    time.sleep(3)
    jobs = driver.find_elements(By.CLASS_NAME, "yKsady")
    for job in jobs:
        data = []
        try:
            job_title = job.find_elements(By.CLASS_NAME, "_15V35X")
            job_description = job.find_elements(By.CLASS_NAME, "_9jGwm1")
            company_name = job.find_elements(By.CLASS_NAME, "Ya0gV9")
            job_posted_date = job.find_elements(By.CLASS_NAME, "e0VAhp")
            location = job.find_elements(By.CLASS_NAME, "_2_Ab4T")
            job_type = job_type
            job_source = "jooble"
            job_source_url = job.find_elements(By.CLASS_NAME, "jkit_ff9zU")[0].get_attribute(
                'href')
            # url_validator = URLValidator()
            # print(url_validator("www.facebook.com"))
            # print(f'Job count number is : {count}')
            # print(f'Job Title is : {job_title[0].text}')
            append_data(data, job_title[0].text)
            # print(f'Company Name is : {company_name[0].text}')
            append_data(data, company_name[0].text)
            # print(f'Location is : {location[0].text}')
            append_data(data, location[0].text)
            # print(f'Job Description is : {job_description[0].text}')
            append_data(data, job_description[0].text)
            # print(f'Job source link is : {job_source_url}')
            append_data(data, job_source_url)
            # print(f'Job Posted Date is : {job_posted_date[0].text}')
            append_data(data, job_posted_date[0].text)
            # print(f'Job source is : {job_source}')
            append_data(data, job_source)
            # print(f'Job type is : {job_type}')
            append_data(data, job_type)
            append_data(data, job_description[0].get_attribute('innerHTML'))
            # print("\n")
            total_job += 1
            scrapped_data.append(data)
        except Exception as e:
            print(e)
        count += 1
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(f'scraper/job_data/jooble - {date_time}.csv', index=False)
    return False, total_job


def append_data(data, field):
    data.append(str(field).strip("+"))


# Create your views here.
def jooble(link, job_type):
    try:
        total_job = 0
        print("Start in try portion. \n")
        scrapped_data = []
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        # driver = webdriver.Chrome('/home/dev/Desktop/selenium')
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
            driver.maximize_window()
            types = link
            job_type = job_type
            try:
                flag = True
                driver.get(types)
                while flag:
                    flag, total_job = find_jobs(driver, scrapped_data, job_type, total_job)
                    print("Fetching...")
            except Exception as e:
                print("out from for loop")
            print("End in try portion. \n")
    except:
        print("Error Occurs. \n")
    ScraperLogs.objects.create(total_jobs=total_job, job_source="Jooble")
