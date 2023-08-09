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
    print("Entered in find_jobs")
    scrapped_data = []
    date_time = str(datetime.now())
    count = 0
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "TwoPane"))
    )
    time.sleep(3)
    # alert = driver.find_elements(By.CLASS_NAME, "jMkAzG")
    # if len(alert) > 0:
    #     alert[0].click()
    jobs = driver.find_elements(By.CLASS_NAME, "SerpJob")

    # try:
    #     for job in jobs:
    #         job.location_once_scrolled_into_view
    #         import pdb
    #         pdb.set_trace()
    # except:
    #     print("")
    # jobs = driver.find_elements(By.CLASS_NAME, "SerpJob")
    for job in jobs:
        data = []
        try:
            job_title = job.find_element(By.CLASS_NAME, "SerpJob-title")
            company_name = job.find_element(By.CLASS_NAME, "SerpJob-company")
            location = job.find_element(By.CLASS_NAME, "SerpJob-location")
            job_type = job_type
            job_source = "workopolis"
            job_source_url = job.find_element(By.CLASS_NAME, "SerpJob-titleLink").get_attribute('href')

            job.click()
            time.sleep(10)
            print(job_title.text)
            job_description = driver.find_element(
                        By.CLASS_NAME, "viewjob-description-tab")
            append_data(data, job_title.text)
            append_data(data, company_name.text)
            append_data(data, location.text)
            append_data(data, job_description.text)
            append_data(data, job_source_url)
            try:
                job_posted_date = job.find_element(By.CLASS_NAME, "ctx-i18n-translated")
                append_data(data, job_posted_date.text)
            except:
                append_data(data, "N/A")
            try:
                flag = False
                try:
                    salary_string = driver.find_element(
                        By.CLASS_NAME, "Salary")
                except:
                    flag = True
                if flag:
                    salary_string = driver.find_element(
                        By.CLASS_NAME, "Estimated_Salary")
                if "$" and "-" in salary_string.text:
                    salary_format = "$"
                    append_data(data, salary_format)
                    estimated_salary = salary_string.text
                    append_data(data, estimated_salary)
                    salary_min = salary_string.text.split(" ")[0]
                    append_data(data, salary_min)
                    salary_max = salary_string.text.split(" ")[2]
                    append_data(data, salary_max)
                else:
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")
            except:
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
    filename = generate_scraper_filename(ScraperNaming.WORKOPOLIS)

    df.to_excel(filename, index=False)
    obj = ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Workopolis", filename=filename)
    return False, total_job


def append_data(data, field):
    data.append(str(field).strip("+"))

def workopolis(link, job_type):
    print("Workopolis")
    try:
        total_job = 0
        options = webdriver.ChromeOptions()  # newly added
        #options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        # with webdriver.Chrome('/home/dev/Desktop/selenium') as driver:
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
