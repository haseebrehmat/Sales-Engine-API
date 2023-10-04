from logging import exception
import sys
import traceback
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming,  k_conversion, configure_webdriver
from utils.helpers import saveLogs


def load_jobs(driver):

    previous_len = len(driver.find_elements(
        By.CLASS_NAME, "hxecsD"))
    print('loading jobs')
    while True:
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        elements = driver.find_elements(By.CLASS_NAME, "hxecsD")
        if previous_len == len(elements):
            break
        previous_len = len(elements)

    return elements


def get_job_urls(driver):
    job_urls = load_jobs(driver)
    links = []
    for job_url in job_urls:
        link = job_url.find_element(By.TAG_NAME, "a")
        link.get_attribute("href")
        t = job_url.find_element(
            By.CLASS_NAME, "new-job-item__JobItemDate-sc-1qa4r36-5")
        links.append([link.get_attribute("href"), t.text])
    return links


def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def find_jobs(driver, job_type):
    scrapped_data = []
    links = get_job_urls(driver)
    total_job = len(links)
    print(total_job)
    original_window = driver.current_window_handle
    for link in links:
        data = []
        if link:
            try:
                driver.switch_to.new_window('tab')
                driver.get(link[0])
                time.sleep(5)
                temp = driver.find_element(
                    By.CLASS_NAME, "JpOdR")
                job_title = temp.find_element(
                    By.CLASS_NAME, "job-title__StyledJobTitle-sc-10irtcq-0")
                append_data(data, job_title.text)

                company_name = driver.find_element(
                    By.CLASS_NAME, "ktyJgG")
                append_data(data, company_name.text.splitlines()[0])

                address = 'Remote'
                append_data(data, address)

                job_source_url = link
                append_data(data, job_source_url)

                job_description = temp
                append_data(data, job_description.text)

               
                job_posted_date = link[1]
                append_data(data, job_posted_date)

                salary_format = "N/A"
                append_data(data, salary_format)

              
                salary_min = "N/A"
                append_data(data, salary_min)
                
                salary_max = "N/A"
                append_data(data, salary_max)
               

                estimated_salary = 'N/A'
                append_data(data, estimated_salary)

                job_source = ScraperNaming.JUST_REMOTE
                append_data(data, job_source)

                job_type = "remote"
                append_data(data, job_type)

                job_description_tags = temp.get_attribute("innerHTML")
                append_data(data, str(job_description_tags))

            except exception as e:
                print(e)

            driver.close()
            driver.switch_to.window(original_window)
            scrapped_data.append(data)

    columns_name = [
        "job_title",
        "company_name",
        "address",
        "job_source_url",
        "job_description",
        "job_posted_date",
        "salary_format",
        "salary_min",
        "salary_max",
        "estimated_salary",
        "job_source",
        "job_type",
        "job_description_tags",
    ]
    
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.JUST_REMOTE)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Just Remote", filename=filename
    )
    return False, total_job


# code starts from here
def just_remote(link, job_type):
    print("Just Remote")

    try:
        driver = configure_webdriver()
        driver.maximize_window()
        flag = True
        try:
            request_url(driver, link)
            while flag:
                flag, _ = find_jobs(driver, job_type)
                print("Fetching...")
            print(SCRAPING_ENDED)

        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)

        driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)


# just_remote('https://justremote.co/remote-jobs', 'remote')
