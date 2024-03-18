import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs

total_job = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    c = 0
    try:
        driver.find_element(By.CLASS_NAME, "clicky").click()
        while True:
            time.sleep(5)
            next_btn = driver.find_elements(By.CLASS_NAME, "next")
            try:
                data = []

                job_title = driver.find_element(
                    By.TAG_NAME, "h1")
                append_data(data, job_title.text)
                company_name = driver.find_element(
                    By.CLASS_NAME, "company")
                append_data(data, company_name.text)
                detail = driver.find_element(By.CLASS_NAME, "details")
                address_span = detail.find_element(By.TAG_NAME, "li")
                address = address_span.find_element(By.TAG_NAME, "span")
                append_data(data, address.text)
                job_description = driver.find_element(
                    By.CLASS_NAME, "content")
                append_data(data, job_description.text)
                append_data(data, driver.current_url)
                job_posted_date = driver.find_elements(By.CLASS_NAME, "badge-r")
                if len(job_posted_date) > 0:
                    append_data(data, job_posted_date[0].text)
                else:
                    append_data(data, 'Posted Today')
                try:
                    salary = driver.find_element(
                        By.CLASS_NAME, "details")
                    estimated_salary = salary.find_elements(By.TAG_NAME, "li")
                    if ' per ' in estimated_salary[1].text:
                        es = estimated_salary[1].text.split(' per ')
                        if 'hour' in es[1]:
                            append_data(data, "hourly")
                        elif ('year' or 'annum') in es[1]:
                            append_data(data, "yearly")
                        elif 'month' in es[1]:
                            append_data(data, "monthly")
                        else:
                            append_data(data, "N/A")
                        append_data(data, k_conversion(es[0]))
                        try:
                            append_data(data, k_conversion(es[0].split('-')[0]))
                        except:
                            append_data(data, "N/A")
                        try:
                            append_data(data, k_conversion(es[0].split('-')[1]))
                        except:
                            append_data(data, "N/A")
                    else:
                        append_data(data, 'N/A')
                        append_data(data, 'N/A')
                        append_data(data, 'N/A')
                        append_data(data, 'N/A')
                except:
                    append_data(data, 'N/A')
                    append_data(data, 'N/A')
                    append_data(data, 'N/A')
                    append_data(data, 'N/A')

                append_data(data, "CareerJet")
                append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))

                scrapped_data.append(data)
                total_job += 1
                try:
                    if len(next_btn) == 0:
                        break
                    else:
                        next_btn[0].click()
                except Exception as e:
                    print(e)
                    break
                c += 1
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.CAREERJET)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="CareerJet", filename=filename)
    return total_job


# code starts from here
def careerjet(link, job_type):
    print("CareerJet")
    driver = configure_webdriver()
    try:
        total_job = 0
        driver.maximize_window()
        try:
            request_url(driver, link)
            driver.maximize_window()
            total_job = find_jobs(driver, job_type, total_job)
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)

    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()
