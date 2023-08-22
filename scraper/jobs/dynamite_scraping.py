import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.models import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming
from utils.helpers import saveLogs
from scraper.utils.helpers import configure_webdriver
total_job = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type, total_job):
    try:
        stop_flag = False
        scrapped_data = []
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "result-item")))

        jobs = driver.find_elements(By.CLASS_NAME, "result-item")

        for job in jobs:
            data = []
            job.click()

            job_details = driver.find_elements(By.CLASS_NAME, "min-h-32")[0].text.split("\n")[:6]

            job_title = job_details[0]
            company_name = job_details[1]
            job_url = driver.find_element(By.CLASS_NAME, 'min-h-32').find_element(By.TAG_NAME, 'a').get_attribute(
                'href')
            if '$' in job_details[3]:
                import pdb
                pdb.set_trace()
                estimated_salary = job_details[-3]
                if 'month' in estimated_salary.split(' per ')[1]:
                    salary_format = 'monthly'
                elif 'hour' in estimated_salary.split(' per ')[1]:
                    salary_format = 'hourly'
                elif ('year' or 'annum') in estimated_salary.split(' per ')[1]:
                    salary_format = 'yearly'
                address = job_details[4]
                job_posted_date = job_details[-1]
            else:
                address = job_details[3]
                estimated_salary = 'N/A'
                salary_format = 'N/A'
                job_posted_date = job_details[-2]

            job_description = driver.find_elements(By.CLASS_NAME, "p-6")[0]

            if '-' in estimated_salary:
                salary = estimated_salary.split('-')
                min_salary = salary[0].strip()
                max_salary = salary[1].split(' per')[0].strip()
            else:
                min_salary = 'N/A'
                max_salary = 'N/A'

            data.append(job_title)
            data.append(company_name)
            data.append(address)
            data.append(job_description.text)
            data.append(job_url)
            data.append(job_posted_date)
            data.append(salary_format)
            data.append(estimated_salary)
            data.append(min_salary)
            data.append(max_salary)
            data.append("Dynamite")
            data.append(job_type)
            data.append(job_description.get_attribute('innerHTML'))
            scrapped_data.append(data)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                        "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                        "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.DYNAMITE)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(df), job_source="Dynamite", filename=filename)
        return not stop_flag, total_job
    except Exception as e:
        saveLogs(e)
        print(f'scrapped stopped due to: {e}')
        return False, total_job


# code starts from here
def dynamite(link, job_type):
    total_job = 0
    print("Dynamite")
    try:
        driver = configure_webdriver(True)
        driver.maximize_window()
        flag = True
        count = 0
        try:
            while flag and count < 15:
                request_url(driver, f'{link}&page={count+1}')
                flag, total_job = find_jobs(driver, job_type, total_job)
                count += 1
                print("Fetching...")  # print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(e)

        driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)

