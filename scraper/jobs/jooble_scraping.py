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
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming

total_job = 0


def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    date_time = str(datetime.now())
    count = 0
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "LKpaAN"))
    )
    time.sleep(3)
    alert = driver.find_elements(By.CLASS_NAME, "jMkAzG")
    if len(alert) > 0:
        alert[0].click()
    jobs = driver.find_elements(By.CLASS_NAME, "LKpaAN")
    try:
        flag = True
        while(flag):
            for job in jobs:
                job.location_once_scrolled_into_view
            # this is the logic for click load more jobs button in this scraper 2 loaders are running
            time.sleep(5)
            jobs = driver.find_elements(By.CLASS_NAME, "LKpaAN")
            for job in jobs:
                job.location_once_scrolled_into_view
            time.sleep(5)
            jobs = driver.find_elements(By.CLASS_NAME, "LKpaAN")
            for job in jobs:
                job.location_once_scrolled_into_view
            time.sleep(5)
            if len(jobs) > 450:
                break
            try:
                driver.find_elements(By.CLASS_NAME, "jkit_AySJs")[1].click()
            except:
                flag = False
    except:
        print("")
    time.sleep(3)
    jobs = driver.find_elements(By.CLASS_NAME, "LKpaAN")
    for job in jobs:
        data = []
        try:
            job_title = job.find_element(By.CLASS_NAME, "jkit_Efecu")
            job_description = job.find_element(By.CLASS_NAME, "EIQN28")
            job_posted_date = job.find_element(By.CLASS_NAME, "klAi0x")
            location = job.find_element(By.CLASS_NAME, "lroapG")
            job_type = job_type
            job_source = "jooble"
            job_source_url = job.find_element(By.CLASS_NAME, "jkit_ff9zU").get_attribute(
                'href')
            append_data(data, job_title.text)
            try:
                company_name = job.find_element(By.CLASS_NAME, "iGX6uI").text
            except:
                company_name = "N/A"
            append_data(data, company_name)
            append_data(data, location.text)
            append_data(data, job_description.text)
            append_data(data, job_source_url)
            append_data(data, job_posted_date.text)
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, job_source)
            append_data(data, job_type)
            append_data(data, job_description.get_attribute('innerHTML'))
            total_job += 1
            scrapped_data.append(data)
        except Exception as e:
            print(e)
        count += 1
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.JOOBLE)

    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Jooble", filename=filename)
    return False, total_job


def append_data(data, field):
    data.append(str(field).strip("+"))


# Create your views here.
def jooble(link, job_type):
    print("Jooble")
    try:
        total_job = 0
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
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
