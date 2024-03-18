import time

import pandas as pd
from selenium.webdriver.common.by import By

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, \
    set_job_type, run_pia_proxy
from utils.helpers import saveLogs


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type):
    scrapped_data = []
    c = 0
    time.sleep(3)
    jobs = driver.find_elements(By.CLASS_NAME, "slider_container")
    for job in jobs:
        try:

            data = []
            time.sleep(1)
            job_posted_date = job.find_element(By.CLASS_NAME, "date")
            try:
                append_data(data, job_posted_date.text.split('\n')[1])
            except:
                append_data(data, 'N/A')

            job.click()
            time.sleep(4)
            append_data(data, job.text.split('\n')[0])
            append_data(data, job.text.split('\n')[1])
            append_data(data, job.text.split('\n')[2])
            job_description = driver.find_element(
                By.CLASS_NAME, "jobsearch-jobDescriptionText")
            append_data(data, job_description.text)
            append_data(data, driver.current_url)
            try:
                estimated_salary = driver.find_element(By.CLASS_NAME, "css-2iqe2o")
                if '$' in estimated_salary.text:
                    a_an = ''
                    if 'an' in estimated_salary.text:
                        a_an = 'an'
                    else:
                        a_an = 'a'
                    if 'hour' in estimated_salary.text.split(a_an)[1]:
                        append_data(data, "hourly")
                    elif ('year' or 'annum') in estimated_salary.text.split(a_an)[1]:
                        append_data(data, "yearly")
                    elif 'month' in estimated_salary.text.split(a_an)[1]:
                        append_data(data, "monthly")
                    else:
                        append_data(data, "N/A")
                    try:
                        append_data(data, k_conversion(estimated_salary.text.split(a_an)[0]))
                    except:
                        append_data(data, "N/A")
                    try:
                        salary_min = estimated_salary.text.split('$')[1]
                        append_data(data, k_conversion(salary_min.split(' ')[0]))
                    except:
                        append_data(data, "N/A")
                    try:
                        salary_max = estimated_salary.text.split('$')[2]
                        append_data(data, k_conversion(salary_max.split(' ')[0]))
                    except:
                        append_data(data, "N/A")
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
            append_data(data, "Indeed")
            append_data(data, set_job_type(job_type))
            append_data(data, job_description.get_attribute('innerHTML'))

            scrapped_data.append(data)
            c += 1
            driver.back()
        except Exception as e:
            print(e)

    columns_name = ["job_posted_date", "job_title", "company_name", "address", "job_description",
                    'job_source_url', "salary_format", "estimated_salary", "salary_min", "salary_max",
                    "job_source", "job_type", "job_description_tags"]

    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.INDEED)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(total_jobs=len(df), job_source="Indeed", filename=filename)

    if not data_exists(driver):
        return False

    next_page = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next Page']")
    next_page.click()
    return True


# check if there is more jobs available or not
def data_exists(driver):
    page_exists = driver.find_elements(By.CSS_SELECTOR, "a[aria-label='Next Page']")
    return False if len(page_exists) == 0 else True

# code starts from here
def indeed(link, job_type):
    print("Indeed")
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        run_pia_proxy(driver, location="mumbai")
        try:
            flag = True
            request_url(driver, link)
            driver.maximize_window()
            while flag:
                flag = find_jobs(driver, job_type)
                print("Fetching...")
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)
    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()