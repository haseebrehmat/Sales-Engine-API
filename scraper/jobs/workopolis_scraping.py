import time
import pandas as pd

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type

total_job = 0

def file_creation(scrapped_data):
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.WORKOPOLIS)

    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Workopolis", filename=filename)
def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    date_time = str(datetime.now())
    count = 0
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "TwoPane"))
    )
    time.sleep(3)
    loop_flag = True
    while(loop_flag):
        jobs = driver.find_elements(By.CLASS_NAME, "SerpJob")
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
                time.sleep(5)
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
                        salary_est = salary_string.text
                        if 'year' in salary_est:
                            salary_format = "yearly"
                        elif 'month' in salary_est:
                            salary_format = "monthly"
                        elif 'hour' in salary_est:
                            salary_format = "hourly"
                        else:
                            salary_format = "N/A"
                        append_data(data, salary_format)
                        estimated_salary = salary_est
                        append_data(data, k_conversion(estimated_salary))
                        salary_min = salary_est.split(" ")[0]
                        append_data(data, k_conversion(salary_min))
                        salary_max = salary_est.split(" ")[2]
                        append_data(data, k_conversion(salary_max))
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
                append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))
                total_job += 1
                scrapped_data.append(data)
            except Exception as e:
                print(e)
            count += 1
        file_creation(scrapped_data)
        from scraper.schedulers.job_upload_scheduler import upload_jobs, remove_files
        upload_jobs('instant scraper', job_source)
        remove_files('instant scraper', job_source)
        scrapped_data = []
        # Here is the login of next page and set the flag of while loop
        try:
            driver.get(driver.find_element(By.CLASS_NAME, "Pagination-link--next").get_attribute('href'))
            time.sleep(5)
        except:
            loop_flag = False
    return False, total_job


def append_data(data, field):
    data.append(str(field).strip("+"))

def workopolis(link, job_type):
    print("Workopolis")
    driver = configure_webdriver()
    try:
        total_job = 0
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
    except:
        print("Error Occurs. \n")
    driver.quit()
