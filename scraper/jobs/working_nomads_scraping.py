import time

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs

def get_job_url(job):
    return job.find_element(By.CLASS_NAME, "open-button").get_attribute('href')


def get_job_detail(driver, job_source, job_url, job_type):
    try:
        job_title = driver.find_element(By.CLASS_NAME, "job-title").text
        company_name = driver.find_element(By.CLASS_NAME, "job-company").text
        job_description = driver.find_element(By.CLASS_NAME, "job")

        job = {
            "job_title": job_title,
            "company_name": company_name,
            "address": "",
            "job_description": job_description.text,
            "job_source_url": job_url,
            "job_posted_date": "",
            "salary_format": "N/A",
            "estimated_salary": "N/A",
            "salary_min": "N/A",
            "salary_max": "N/A",
            "job_source": job_source,
            "job_type": set_job_type(job_type),
            "job_description_tags": job_description.get_attribute('innerHTML')
        }

        about_job_lines = driver.find_elements(By.CLASS_NAME, "about-job-line")

        for about_line in about_job_lines:
            # class_name is class of i icon, fetch data on the bases of icons classes
            class_name = about_line.find_element(By.CLASS_NAME, 'fa').get_attribute('class')
            about_line_text = about_line.find_element(By.CLASS_NAME, 'about-job-line-text').text
            if 'fa-calendar' in class_name:
                job['job_posted_date'] = about_line_text
            elif 'fa-map-marker' in class_name:
                job['address'] = about_line_text
            elif 'fa-money' in class_name:
                # save salary data
                if 'year' in about_line_text:
                    job['salary_format'] = 'yearly'
                else:
                    job['salary_format'] = 'N/A'
                job['estimated_salary'] = k_conversion(about_line_text)
                salary = about_line_text.split('-')
                job['salary_min'] = k_conversion(salary[0] if '-' in about_line_text else about_line_text.split(' ')[0])
                job['salary_max'] = k_conversion(salary[1].split(' ')[0] if '-' in about_line_text else about_line_text.split(' ')[0])
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
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "job-desktop")))
        try:
            for i in range(0, 40):
                show_more_btn = driver.find_element(By.CLASS_NAME, "show-more")
                show_more_btn.click()
                time.sleep(3)
        except Exception as e:
            print('Loaded all jobs ...')
            saveLogs(e)

        jobs = driver.find_elements(By.CLASS_NAME, "job-desktop")
        job_urls = []

        for job in jobs:
            job_posted_date = job.find_elements(By.CLASS_NAME, 'date')[2].text
            if 'days ago' in job_posted_date:
                days = int(job_posted_date.split(' ')[0])
                if days > 3:
                    break
            job_urls.append(get_job_url(job))

        count = 0
        total_jobs = len(job_urls)

        for job_url in job_urls:
            try:
                driver.get(job_url)
                job, error = get_job_detail(driver, 'workingnomads', job_url, job_type)
                if error:
                    break
                data = [job[c] for c in columns_name]
                scrapped_data.append(data)
                # upload jobs by 20 records
                count += 1

                if scrapped_data and count > 0 and (count%20 == 0 or count == total_jobs - 1):
                    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
                    filename = generate_scraper_filename(ScraperNaming.WORKING_NOMADS)
                    df.to_excel(filename, index=False)
                    ScraperLogs.objects.create(total_jobs=len(df), job_source='Working Nomads', filename=filename)
                    scrapped_data = []
            except Exception as e:
                print(e)
                saveLogs(e)
                break
    except Exception as e:
        saveLogs(e)


def working_nomads(link, job_type):
    driver = configure_webdriver()
    try:
        print("Start in try portion. \n")
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
