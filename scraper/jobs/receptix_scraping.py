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
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type, k_conversion
from utils.helpers import saveLogs


def get_job_url(job):
    return job.get_attribute('href')


def find_jobs(driver, job_type):
    scrapped_data = []
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                    "job_description_tags"]
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "displaying-all-jobs")))
        # get links of jobs
        jobs = driver.find_elements(By.CLASS_NAME, "displaying-all-jobs")
        job_urls = [get_job_url(job) for job in jobs]

        # scrap job 1 by 1
        for job_url in job_urls:
            try:
                driver.get(job_url)
                job, error = get_job_detail(driver, 'receptix', job_url, job_type)
                if not error:
                    data = [job[c] for c in columns_name]
                    scrapped_data.append(data)
            except Exception as e:
                print(e)
                saveLogs(e)
                break

        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.RECEPTIX)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(df), job_source='Receptix', filename=filename)
        return True
    except Exception as e:
        saveLogs(e)
        return False

def get_job_detail(driver, job_source, job_url, job_type):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.secondary-font-style")))
        job_title = driver.find_element(By.CSS_SELECTOR, "h1.secondary-font-style").text
        company_name = driver.find_element(By.TAG_NAME, "h4").text
        job_description = driver.find_element(By.CLASS_NAME, "job-descrptn-main-div")

        job = {"job_title": job_title, "company_name": company_name, "address": "",
            "job_description": job_description.text, "job_source_url": job_url, "job_posted_date": "",
            "salary_format": "N/A", "estimated_salary": "N/A", "salary_min": "N/A", "salary_max": "N/A",
            "job_source": job_source, "job_type": set_job_type(job_type),
            "job_description_tags": job_description.get_attribute('innerHTML')}


        try:
            job['job_posted_date'] = driver.find_element(By.CLASS_NAME, 'job-post-text-p').text.split(':')[1]
        except Exception as e:
            print(e)
        try:
            job['address'] = driver.find_element(By.CLASS_NAME, 'job-locations').text.split(':')[1]
        except Exception as e:
            print(e)
        return job, False
    except Exception as e:
        saveLogs(e)
        return None, True


def append_data(data, field):
    data.append(str(field).strip("+"))


def receptix(link, job_type):
    print("Receptix Scraper starter")
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        try:
            flag = True
            page = 0
            while page < 50 and flag:
                driver.get(f'{link}?page={page+1}')
                print("Fetching...")
                flag = find_jobs(driver, job_type)
                page += 1
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
    driver.quit()
