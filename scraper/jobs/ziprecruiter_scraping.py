from datetime import datetime
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs
from settings.utils.helpers import generate_random_email

def submit_email_alert(driver):
    # submit modal for email notifcation
    form_submitted = False
    try:
        driver.find_element(By.NAME, "email_address").send_keys(generate_random_email())
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'zrs_btn_primary_400').submit()
        time.sleep(3)
        form_submitted = True
    except Exception as e:
        print(e)
    if not form_submitted:
        try:
            driver.find_element(By.CLASS_NAME, 'text-button-primary-default-text').click()
        except Exception as e:
            print(e)
    time.sleep(3)


def get_job_url(job):
    return job.find_element(By.CLASS_NAME, "job_link").get_attribute('href')


def get_job_detail(driver, job_source, job_url, job_type):
    try:
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, "job_title")))
        job_title = driver.find_element(By.CLASS_NAME, "job_title").text
        company_name = driver.find_element(By.CLASS_NAME, "hiring_company").text
        job_description = driver.find_element(By.CLASS_NAME, "job_description")
        address = driver.find_element(By.CLASS_NAME, 'hiring_location').text

        job = {
            "job_title": job_title,
            "company_name": company_name,
            "address": address,
            "job_description": job_description.text,
            "job_source_url": job_url,
            "job_posted_date": 'N/A',
            "salary_format": "N/A",
            "estimated_salary": "N/A",
            "salary_min": "N/A",
            "salary_max": "N/A",
            "job_source": job_source,
            "job_type": set_job_type(job_type),
            "job_description_tags": job_description.get_attribute('innerHTML')
        }

        for single_job in driver.find_elements(By.XPATH, "//p[@class='job_more']"):
            if 'Posted date:' in single_job.text:
                job['job_posted_date'] = single_job.text
        try:
            job_est_sal = driver.find_element(
                By.CLASS_NAME, 't_compensation').text
            job['estimated_salary'] = k_conversion(job_est_sal.split(' per ')[0])
            job['salary_format'] = job_est_sal.split(' per ')[1]
            if 'year' in job['salary_format']:
                job['salary_format'] = 'yearly'
            elif 'hour' in job['salary_format']:
                job['salary_format'] = 'hourly'
            else:
                job['salary_format'] = 'N/A'
            try:
                job['salary_min'] = k_conversion(job['estimated_salary'].split(' to ')[0])
            except:
                job['salary_min'] = 'N/A'
            try:
                job['salary_max'] = k_conversion(job['estimated_salary'].split(' to ')[1])
            except:
                job['salary_max'] = 'N/A'

        except:
            job['estimated_salary'] = "N/A"
            job['salary_format'] = "N/A"
            job['salary_min'] = "N/A"
            job['salary_max'] = "N/A"
        return job, False
    except Exception as e:
        saveLogs(e)
        return None, True

def pagination_available(driver):
    try:
        driver.find_element(By.CLASS_NAME, 'load_more_btn')
        return False
    except Exception as e:
        print(e)
        return True

def find_jobs(driver, job_type):
    scrapped_data = []
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                    "job_description_tags"]
    try:
        submit_email_alert(driver)
        time.sleep(4)
        pagination_flag = pagination_available(driver)
        job_urls = []
        if pagination_flag:
            for i in range(30):
                try:
                    jobs = driver.find_elements(By.CLASS_NAME, 'group')
                    job_links = [job.find_element(By.TAG_NAME, 'a').get_attribute('href') for job in jobs]
                    job_urls.extend(job_links)
                    next_page_link = driver.find_elements(By.CLASS_NAME, 'prev_next_page_btn')[1].get_attribute('href')
                    if driver.current_url != next_page_link:
                        driver.get(next_page_link)
                        time.sleep(3)
                    else:
                        break
                except Exception as e:
                    print(e)
        else:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "job_item")))
            try:
                time.sleep(6)
                jobs = []
                for i in range(25):
                    old_jobs_count = len(jobs)
                    jobs = driver.find_elements(By.CLASS_NAME, "job_item")
                    time.sleep(3)
                    if i == 0:
                        driver.find_element(By.CLASS_NAME, 'load_more_btn').click()
                        time.sleep(5)
                    if len(jobs) > 2:
                        jobs[-1].location_once_scrolled_into_view
                        jobs[-2].location_once_scrolled_into_view
                    for job in jobs:
                        job.location_once_scrolled_into_view
                    time.sleep(5)
                    if old_jobs_count == len(jobs):
                        break
            except Exception as e:
                print('Loaded all jobs ...')
                saveLogs(e)
            jobs = driver.find_elements(By.CLASS_NAME, "job_item")
            job_urls = [get_job_url(job) for job in jobs]

        count = 0
        job_urls = list(filter(lambda link: 'https://www.ziprecruiter.com/k' in link, job_urls))
        total_jobs = len(job_urls)

        for job_url in job_urls:
            try:
                driver.get(job_url)
                job, error = get_job_detail(driver, 'ziprecruiter', job_url, job_type)
                if not error:
                    data = [job[c] for c in columns_name]
                    scrapped_data.append(data)
                    time.sleep(2)
                count += 1

                # upload jobs in chunks of 20 size
                if scrapped_data and count > 0 and (count % 20 == 0 or count == total_jobs - 1):
                    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
                    filename = generate_scraper_filename(ScraperNaming.ZIP_RECRUITER)
                    df.to_excel(filename, index=False)
                    ScraperLogs.objects.create(total_jobs=len(df), job_source='Zip Recruiter', filename=filename)
                    scrapped_data = []

            except Exception as e:
                print(e)
                saveLogs(e)
                break
    except Exception as e:
        saveLogs(e)


def ziprecruiter_scraping(link, job_type):
    print('Zip Recruiter')
    try:
        print("Start in try portion. \n")
        driver = configure_webdriver()
        driver.maximize_window()
        try:
            driver.get(link)
            print("Fetching...")
            find_jobs(driver, job_type)
        except Exception as e:
            saveLogs(e)
            print("out from for loop")
        driver.quit()
    except Exception as e:
        saveLogs(e)
        print("Error Occurs. \n")
