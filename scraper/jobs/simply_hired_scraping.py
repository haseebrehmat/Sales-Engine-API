import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, \
    set_job_type
from utils.helpers import saveLogs


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type, next_page_no):
    scrapped_data = []
    count = 0
    time.sleep(3)
    jobs = driver.find_elements(By.CLASS_NAME, "css-1y7j4hn")

    es = driver.find_elements(By.CLASS_NAME, "css-1ejkpji")

    for job in jobs:
        data = []
        try:
            job.click()
            time.sleep(5)

            append_data(data, job.text)
            context = driver.find_elements(By.CLASS_NAME, "css-xtodu4")
            company_name = context[0].text.split("-")
            append_data(data, company_name[0])
            address = context[1].text
            append_data(data, address)
            job_description = driver.find_element(By.CLASS_NAME, "css-cxpe4v")
            append_data(data, job_description.text)
            append_data(data, job.get_attribute('href'))
            try:
                job_posted_date = context[4].text
            except Exception as e:
                job_posted_date = 'Today'
            append_data(data, job_posted_date)
            try:
                estimated_salary = es[count].text.split(" a")[0]
                if '$' in estimated_salary:
                    append_data(data, "N/A")
                if "d: " in estimated_salary:
                    estimated_salary = estimated_salary.split(": ")[1]
                if "to " in estimated_salary:
                    estimated_salary = estimated_salary.split("to ")[1]
                append_data(data, k_conversion(estimated_salary))
                try:
                    append_data(data, k_conversion(estimated_salary.split(' - ')[0]))
                except:
                    append_data(data, "N/A")
                try:
                    append_data(data, k_conversion(estimated_salary.split(' - ')[1]))
                except:
                    append_data(data, "N/A")
            except:
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")

            append_data(data, "Simplyhired")
            append_data(data, set_job_type(job_type))
            append_data(data, job_description.get_attribute('innerHTML'))

            scrapped_data.append(data)
        except Exception as e:
            print(e)
        count += 1


    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.SIMPLY_HIRED)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Simply Hired", filename=filename)

    if not data_exists(driver):
        return False

    try:
        next_page = driver.find_elements(By.CLASS_NAME, "css-1wxsdwr")
        next_page_clicked = False
        for i in next_page:
            if i.text == f'{next_page_no}':
                i.click()
                next_page_clicked = True
                break
        return next_page_clicked
    except Exception as e:
        return False

# check if there is more jobs available or not
def data_exists(driver):
    pagination = driver.find_elements(By.CLASS_NAME, "css-gxlopd")
    return False if len(pagination) == 0 else True


# code starts from here
def simply_hired(link, job_type):
    print("Simply hired")
    try:
        driver = configure_webdriver()
        driver.maximize_window()
        try:
            flag = True
            page_no = 2
            request_url(driver, link)
            while flag and page_no <= 40:
                flag = find_jobs(driver, job_type, page_no)
                page_no += 1
                print("Fetching...")
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)

        driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)
