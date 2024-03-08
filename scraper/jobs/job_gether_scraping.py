import time

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type
from utils.helpers import saveLogs

def get_job_url(job):
    return job.find_element(By.CLASS_NAME, "open-button").get_attribute('href')


def get_job_detail(driver, job_source, job_url, job_date, job_type):
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "opportunity_info_title")))
        time.sleep(3)
        for i in range(3):
            try:
                driver.find_element(By.CLASS_NAME, 'see_more_button').find_element(By.TAG_NAME, 'span').click()
                time.sleep(3)
                see_more_text = driver.find_element(By.CLASS_NAME, 'see_more_button').find_element(By.TAG_NAME, 'span').text
                if see_more_text.lower() != 'see more':
                    break
            except Exception as e:
                saveLogs(e)
        job_title = driver.find_element(By.CLASS_NAME, "opportunity_info_title").text
        company_name = driver.find_element(By.CLASS_NAME, "company-name").text
        job_description = driver.find_element(By.ID, "description_container")

        job = {
            "job_title": job_title,
            "company_name": company_name,
            "address": "",
            "job_description": job_description.text,
            "job_source_url": job_url,
            "job_posted_date": job_date,
            "salary_format": "N/A",
            "estimated_salary": "N/A",
            "salary_min": "N/A",
            "salary_max": "N/A",
            "job_source": job_source,
            "job_type": set_job_type(job_type),
            "job_description_tags": job_description.get_attribute('innerHTML')
        }

        job_general_info = driver.find_element(By.CSS_SELECTOR, "#offer_general_data").text.replace(':\n', ':').replace('\nK', 'K').split('\n')

        try:
            for item in job_general_info:
                info_detail = item.split(':')
                key = info_detail[0].lower()
                val = info_detail[1].lower()
                if key == 'work from':
                    job['address'] = val
                elif key == 'salary':
                    job['estimated_salary'] = val
                    if 'year' in val:
                        job['salary_format'] = 'yearly'
                    elif 'month' in val:
                        job['salary_format'] = 'monthly'
                    elif 'hour' in val:
                        job['salary_format'] = 'hourly'
                    if '-' in val:
                        salary = val.split(' - ')
                        factor = 3 if 'k' in val else 0
                        job['salary_min'] = salary[0].replace('k', '') + '0' * factor
                        job['salary_max'] = salary[1].split('k ')[0] + '0' * factor
                    else:
                        job['salary_min'] = val
                        job['salary_max'] = val
        except Exception as e:
            saveLogs(e)
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
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "match-card")))
        try:
            for i in range(20):
                jobs = driver.find_elements(By.CLASS_NAME, "match-card")
                for job in jobs:
                    job.location_once_scrolled_into_view
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR, 'a.btn-primary').click()
                time.sleep(5)
        except Exception as e:
            print('Loaded all jobs ...')
            saveLogs(e)

        jobs = driver.find_elements(By.CLASS_NAME, "match-card")
        job_urls = []

        for job in jobs:
            job_posted_date = job.find_element(By.CLASS_NAME, 'date_fav_container').text
            url = job.find_element(By.CLASS_NAME, 'offer-link').get_attribute('href')
            job_urls.append({'url': url, 'date': job_posted_date})

        count = 0
        total_jobs = len(job_urls)

        for job_url in job_urls:
            try:
                url = job_url['url']
                date = job_url['date']
                driver.get(url)
                job, error = get_job_detail(driver, 'jobgether', url, date, job_type)
                if error:
                    break
                data = [job[c] for c in columns_name]
                scrapped_data.append(data)
                # upload jobs by 20 records
                count += 1

                if scrapped_data and count > 0 and (count%20 == 0 or count == total_jobs - 1):
                    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
                    filename = generate_scraper_filename(ScraperNaming.JOB_GETHER)
                    df.to_excel(filename, index=False)
                    ScraperLogs.objects.create(total_jobs=len(df), job_source='Job Gether', filename=filename)
                    scrapped_data = []
            except Exception as e:
                print(e)
                saveLogs(e)
                break
    except Exception as e:
        saveLogs(e)


def job_gether(link, job_type):
    print("Job Gether")
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        try:
            driver.get(link)
            print("Fetching...")
            find_jobs(driver, job_type)
        except Exception as e:
            saveLogs(e)
            print("out from for loop")
    except Exception as e:
        saveLogs(e)
        print("Error Occurs. \n")
    driver.quit()
