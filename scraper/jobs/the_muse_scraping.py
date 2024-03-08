import time

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type
from utils.helpers import saveLogs

def get_job_url(job):
    return job.find_element(By.CLASS_NAME, "JobCard_viewJobLink__Gesny").get_attribute('href')


def get_job_detail(driver, job_source, job_url, job_type):
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "JobIndividualHeader_jobHeaderTitle__wA3d3")))
        job_title = driver.find_element(By.CLASS_NAME, "JobIndividualHeader_jobHeaderTitle__wA3d3").text
        company_name = driver.find_element(By.CLASS_NAME, "JobIndividualHeader_jobHeaderCompanyName__PKqdn").text
        job_description = driver.find_element(By.CLASS_NAME, "JobIndividualBody_jobBodyContainer__rQGA_")

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
            "job_type": set_job_type(job_type),
            "job_description_tags": job_description.get_attribute('innerHTML')
        }

        try:
            job_info = driver.find_element(By.CLASS_NAME, 'JobIndividualHeader_jobHeaderSubHeading__nRAGH').text.split('•')
            job['job_posted_date'] = job_info[0]
            job['address'] = job_info[1]
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
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "JobCard_jobCardClickable__ZR6Sk")))
        try:
            for i in range(45):
                jobs = driver.find_elements(By.CLASS_NAME, "JobCard_jobCardClickable__ZR6Sk")
                for job in jobs:
                    job.location_once_scrolled_into_view
                time.sleep(3)
                driver.find_element(By.CLASS_NAME, 'LoadMore_loadMore__Gi4JP').click()
                time.sleep(3)
        except Exception as e:
            print('Loaded all jobs ...')
            saveLogs(e)

        jobs = driver.find_elements(By.CLASS_NAME, "JobCard_jobCardClickable__ZR6Sk")
        job_urls = [get_job_url(job) for job in jobs]

        count = 0
        total_jobs = len(job_urls)

        for job_url in job_urls:
            try:
                driver.get(job_url)
                job, error = get_job_detail(driver, 'themuse', job_url, job_type)
                if error:
                    break
                data = [job[c] for c in columns_name]
                scrapped_data.append(data)
                # upload jobs by 20 records
                count += 1

                if scrapped_data and count > 0 and (count%20 == 0 or count == total_jobs - 1):
                    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
                    filename = generate_scraper_filename(ScraperNaming.THE_MUSE)
                    df.to_excel(filename, index=False)
                    ScraperLogs.objects.create(total_jobs=len(df), job_source='The Muse', filename=filename)
                    scrapped_data = []
            except Exception as e:
                print(e)
                saveLogs(e)
                break
    except Exception as e:
        saveLogs(e)


def the_muse(link, job_type):
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
