import time
from datetime import datetime
from scraper.models.accounts import Accounts
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


def login(driver, email, password):
    try:
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "email-input").click()
        driver.find_element(By.ID, "inlineUserEmail").clear()
        driver.find_element(By.ID, "inlineUserEmail").send_keys(
            email)
        driver.find_element(By.CLASS_NAME, "email-button").click()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "password-input").click()
        driver.find_element(By.ID, "inlineUserPassword").clear()
        driver.find_element(By.ID, "inlineUserPassword").send_keys(
            password)
        driver.find_element(By.CLASS_NAME, "css-jbcabp").click()
        login = driver.find_elements(By.CLASS_NAME, "iconContainer")
        if len(login) > 0:
            return False
        time.sleep(5)
        return True
    except Exception as e:
        print(e)
        return False


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    count = 0
    c_count = 0
    time.sleep(3)
    try:
        jobs = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__JBBUV")
        for job in jobs:
            try:
                data = []
                job.click()
                time.sleep(3)
                job_detail = job.text.split('\n')
                append_data(data, job_detail[1])
                append_data(data, job_detail[0])
                append_data(data, job_detail[2])
                try:
                    driver.find_element(By.CLASS_NAME, "JobDetails_showMore__j5Z_h").click()
                    time.sleep(0.5)
                except:
                    pass
                job_description = driver.find_element(By.CLASS_NAME, "JobDetails_jobDescription__6VeBn")
                append_data(data, job_description.text)
                url = job.find_element(By.CLASS_NAME, "jobCard")
                append_data(data, url.get_attribute('href'))
                try:
                    append_data(data, job_detail[-1])
                except Exception as e:
                    append_data(data, "24h")
                try:
                    estimated_salary = job.find_element(By.CLASS_NAME, "salary-estimate")
                    es = estimated_salary.text.split(' (')[0]
                    if 'Per' in es:
                        es_salary = es.split(" Per ")
                        salary_format = es_salary[1]
                        if 'Hour' in salary_format:
                            append_data(data, "hourly")
                        elif 'Month' in salary_format:
                            append_data(data, "monthly")
                        elif ('Year' or 'Annum') in salary_format:
                            append_data(data, "yearly")
                        else:
                            append_data(data, "N/A")
                    else:
                        append_data(data, 'N/A')
                    append_data(data, k_conversion(es))
                    try:
                        append_data(data, k_conversion(es.split(" - ")[0].split(" Per")[0]))
                    except:
                        append_data(data, "N/A")
                    try:
                        append_data(data, k_conversion(es.split(" - ")[1].split(" Per")[0]))
                    except:
                        append_data(data, "N/A")

                    c_count += 1
                except:
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")

                append_data(data, "Glassdoor")
                append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))
                scrapped_data.append(data)
                count += 1
                total_job += 1
            except Exception as e:
                print(e)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]

        filename = generate_scraper_filename(ScraperNaming.GLASSDOOR)
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Glassdoor", filename=filename)
    except Exception as e:
        saveLogs(e)
        print(e)


def load_jobs(driver):
    try:
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "button_Button__meEg5").click()
        return True
    except Exception as e:
        return False


# code starts from here
def glassdoor(link, job_type):
    print("Glassdoor")
    exit_scraping = False
    try:
        for x in Accounts.objects.all():
            total_job = 0
            driver = configure_webdriver()
            driver.maximize_window()
            request_url(driver, GLASSDOOR_LOGIN_URL)
            logged_in = login(driver, x.email, x.password)
            try:
                if logged_in:
                    flag = True
                    request_url(driver, link)
                    while flag:
                        flag = load_jobs(driver)
                    find_jobs(driver, job_type, total_job)
                    print(SCRAPING_ENDED)
                    exit_scraping = True
                else:
                    print(LOGIN_FAILED)
                    exit_scraping = False
            except Exception as e:
                saveLogs(e)
                print(LINK_ISSUE)
                exit_scraping = True
            driver.quit()
            if exit_scraping:
                break
    except Exception as e:
        saveLogs(e)
        print(e)
