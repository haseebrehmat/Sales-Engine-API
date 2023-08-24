import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver
from utils.helpers import saveLogs

total_job = 0

def save_data(scrapped_data, job_title, company_name, address, job_description, job_source_url, salary_format, estimated_salary, salary_min, salary_max, job_type, job_description_tags):
    try:
        data = []
        append_data(data, job_title)
        append_data(data, company_name)
        append_data(data, address)
        append_data(data, job_description)
        append_data(data, job_source_url)
        append_data(data, "N/A")
        append_data(data, salary_format)
        append_data(data, k_conversion(estimated_salary))
        append_data(data, k_conversion(salary_min))
        append_data(data, k_conversion(salary_max))
        append_data(data, "YCombinator")
        append_data(data, job_type)
        append_data(data, job_description_tags)
        scrapped_data.append(data)
    except Exception as e:
        print(e)

def finding_job(driver, company_name, scrapped_data):
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "bg-beige-lighter"))
        )
        job_title = driver.find_element(By.CLASS_NAME, "company-name").text
        details = driver.find_elements(By.CLASS_NAME, "company-details")
        details_loc = details[1].find_elements(By.TAG_NAME, "div")
        address = details_loc[0].text
        job_type = details_loc[2].text
        description = driver.find_element(By.CLASS_NAME, "bg-beige-lighter")
        job_description = description.find_elements(By.TAG_NAME, "div")

        desc = ""
        desc_tags = ""
        for i in range(1, len(job_description)):
            desc += job_description[i].text
            desc_tags += job_description[i].get_attribute('innerHTML')

        job_source_url = driver.current_url
        salary = driver.find_element(By.CLASS_NAME, "company-title")
        slr = salary.find_elements(By.TAG_NAME, "div")
        if len(slr) > 0 and slr[0].text != '':
            estimated_salary = slr[0].find_element(By.TAG_NAME, "span").text
            if '-' in estimated_salary:
                salary_min = estimated_salary.split(' - ')[0]
                salary_max = estimated_salary.split(' - ')[1]
                salary_format = 'N/A'
            else:
                salary_min = estimated_salary.split('K')[0]
                salary_max = estimated_salary.split('K')[0]
                salary_format = 'N/A'
        else:
            salary_format = 'N/A'
            estimated_salary = 'N/A'
            salary_min = 'N/A'
            salary_max = 'N/A'

        save_data(scrapped_data, job_title, company_name, address, desc, job_source_url, salary_format, estimated_salary, salary_min, salary_max, job_type, desc_tags)
    except Exception as e:
        print(e)

def company_jobs(driver, scrapped_data):
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "job-name"))
        )
        job_name = driver.find_elements(By.CLASS_NAME, "job-name")
        for job in job_name:
            try:
                link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
                company_name = driver.find_element(By.CLASS_NAME, "company-name").text
                original_window = driver.current_window_handle
                driver.switch_to.new_window('tab')
                driver.get(link)
                finding_job(driver, company_name, scrapped_data)
                driver.close()
                driver.switch_to.window(original_window)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

def loading(driver):
    while True:
        try:
            time.sleep(3)
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "loading"))
            )
            load = driver.find_elements(By.CLASS_NAME, "loading")
            if len(load) > 0:
                load[0].location_once_scrolled_into_view
            else:
                break
        except Exception as e:
            break

def login(driver):
    try:
        # WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located(
        #         (By.CLASS_NAME, "MuiTypography-root"))
        # )
        time.sleep(10)
        driver.find_element(By.CLASS_NAME, "MuiTypography-root").click()
        time.sleep(10)
        # WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located(
        #         (By.CLASS_NAME, "input-group"))
        # )
        driver.find_elements(By.CLASS_NAME, "input-group")[3].click()
        time.sleep(10)
        email = driver.find_elements(By.CLASS_NAME, "MuiInput-input")[3]
        email.clear()
        email.send_keys(Y_EMAIL)
        time.sleep(10)

        driver.find_elements(By.CLASS_NAME, "input-group")[4].click()
        time.sleep(10)
        password = driver.find_elements(By.CLASS_NAME, "MuiInput-input")[4]
        password.clear()
        password.send_keys(Y_PASSWORD)
        time.sleep(10)

        driver.find_element(By.CLASS_NAME, "sign-in-button").click()
        time.sleep(20)

        return True
    except Exception as e:
        return False


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, total_job):
    c = 0
    try:
        companies = driver.find_elements(By.CLASS_NAME, "text-2xl")
        scrapped_data = []
        for i in range(1, len(companies)):
            try:
                link = companies[i].find_elements(By.TAG_NAME, "a")[0].get_attribute('href')
                original_window = driver.current_window_handle
                driver.switch_to.new_window('tab')
                driver.get(link)
                company_jobs(driver, scrapped_data)
                driver.close()
                driver.switch_to.window(original_window)
                passed = True
            except Exception as e:
                print(e)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.YCOMBINATOR)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="YCombinator", filename=filename)

    except Exception as e:
        print(e)


# code starts from here
def ycombinator(link, job_type):
    print("YCombinator")
    try:
        total_job = 0
        driver = configure_webdriver()
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, YCOMBINATOR_LOGIN_URL)
            driver.maximize_window()
            if login(driver):
                request_url(driver, link)
                loading(driver)
                find_jobs(driver, total_job)
            else:
                print("Login failed")
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)

        driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)
