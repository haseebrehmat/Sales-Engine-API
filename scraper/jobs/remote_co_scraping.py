import time

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver
from utils.helpers import saveLogs

def get_job_url(job):
    return job.get_attribute('href')


def get_job_detail(driver, job_source, job_url, job_type):
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.font-weight-bold")))
        job_headline = driver.find_element(By.CSS_SELECTOR, "h1.font-weight-bold").text.split(' at ')
        job_title = job_headline[0]
        company_name = job_headline[1]
        job_description = driver.find_element(By.CLASS_NAME, "job_description")

        job = {
            "job_title": job_title,
            "company_name": company_name,
            "address": "",
            "job_description": job_description.text,
            "job_source_url": job_url,
            "job_posted_date": 'N/A',
            "salary_format": "N/A",
            "estimated_salary": "N/A",
            "salary_min": "N/A",
            "salary_max": "N/A",
            "job_source": job_source,
            "job_type": job_type,
            "job_description_tags": job_description.get_attribute('innerHTML')
        }

        try:
            job['job_posted_date'] = driver.find_element(By.TAG_NAME, 'time').text.replace('Posted: ', '')
        except Exception as e:
            print(e)
        try:
            job['address'] = driver.find_element(By.CLASS_NAME, 'location_sm').text.replace('Location: ', '')
        except Exception as e:
            print(e)
        try:
            salary_info = driver.find_element(By.CLASS_NAME, 'salary_sm').text.replace('Salary: ', '').replace(',', '').lower()
            if 'year' in salary_info or 'month' in salary_info or 'annual' in salary_info or 'hour' in salary_info:
                salary_data = salary_info.split(' ')
                job["salary_format"] = salary_data[-1]
                job["estimated_salary"] = salary_data[0]
                job["salary_min"] = salary_data[0]
                job["salary_max"] = salary_data[0]
        except Exception as e:
            print(e)
        return job, False
    except Exception as e:
        saveLogs(e)
        return None, True

def find_jobs(driver, job_type):
    scrapped_data = []

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                    "job_description_tags"]
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "job-card")))
        jobs = driver.find_elements(By.CSS_SELECTOR, 'div.card  div.card-body > a')[:-1]
        job_urls = [get_job_url(job) for job in jobs]
        current_url = driver.current_url
        count = 0
        total_jobs = len(job_urls)

        for job_url in job_urls:
            try:
                driver.get(job_url)
                job, error = get_job_detail(driver, 'remoteco', job_url, job_type)
                if not error:
                    data = [job[c] for c in columns_name]
                    scrapped_data.append(data)
                    # upload jobs by 20 records
                    count += 1

                if scrapped_data and count > 0 and (count%20 == 0 or count == total_jobs - 1):
                    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
                    filename = generate_scraper_filename(ScraperNaming.REMOTE_CO)
                    df.to_excel(filename, index=False)
                    ScraperLogs.objects.create(total_jobs=len(df), job_source='Remote CO', filename=filename)
                    scrapped_data = []
            except Exception as e:
                print(e)
                saveLogs(e)
                return False
        driver.get(current_url)
        pagination = driver.find_element(By.CLASS_NAME, 'next')
        if pagination.get_attribute('class').find('disabled') != -1:
            return False
        pagination.click()
        time.sleep(3)
        return True
    except Exception as e:
        saveLogs(e)
        return False


def remote_co(link, job_type):
    print('Remote CO Scraper ... ')
    driver = configure_webdriver(block_media=True)
    try:
        print("Start in try portion. \n")
        driver.maximize_window()
        try:
            driver.get(link)
            print("Fetching...")
            flag = True
            while flag:
                flag = find_jobs(driver, job_type)
        except Exception as e:
            saveLogs(e)
            print("out from for loop")
    except Exception as e:
        saveLogs(e)
        print("Error Occurs. \n")
    driver.quit()
