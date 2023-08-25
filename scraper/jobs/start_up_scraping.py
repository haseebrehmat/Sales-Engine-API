import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver
from utils.helpers import saveLogs

total_job = 0
links = [
    "https://startup.jobs/?remote=true&q=data+scientist",
    "https://startup.jobs/?q=software"
]

jobs_query_selector = '//*[@id="posts-index"]/section[2]/div/div/div[2]/div'
next_pagination_selector = "/html/body/section[2]/div/div/a"
job_title_selector = "div.col-span-6.flex.items-center.gap-3 > div > a.pt-1.block.font-medium.seen\:font-normal.seen"
location_selector = "jobListing__main__meta__location"
job_description_selector = "trix-content"
remote_selector = "jobListing__main__meta__remote"
max_scrap_limit = 2000


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    date_time = str(datetime.now())
    count = 0
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grid"))
    )
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        next_page = driver.find_element(By.XPATH, next_pagination_selector).text.lower() == "show more results"

        while next_page and count <= max_scrap_limit:
            main_tab_handle = driver.current_window_handle
            jobs = driver.find_elements(By.XPATH, jobs_query_selector)
            try:
                for idx, job in enumerate(jobs):
                    if count >= max_scrap_limit:
                        break
                    try:
                        job = job.find_element(By.CLASS_NAME, "items-start")
                        job_title, company_name = job.text.split("\n")
                        job_source_url = job.find_element(By.TAG_NAME, "a").get_attribute("href")
                        job.find_element(By.TAG_NAME, "a").click()
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        # Perform scraping or other operations on the product detail page
                        # ...
                        try:
                            address = driver.find_element(By.CLASS_NAME, location_selector).text
                        except:
                            address = driver.find_element(By.CLASS_NAME, remote_selector).text

                        job_description_tags = driver.find_element(By.CLASS_NAME, job_description_selector).get_attribute("outerHTML")
                        job_description = driver.find_element(By.CLASS_NAME, job_description_selector).text
                        job_posted_date = "N/A"
                        salary_format = "N/A"
                        estimated_salary = "N/A"
                        salary_min = "N/A"
                        salary_max = "N/A"
                        job_source = "startup"
                        data = []
                        append_data(data, job_title)
                        append_data(data, company_name)
                        append_data(data, address)
                        append_data(data, job_description)
                        append_data(data, job_source_url)
                        append_data(data, job_posted_date)
                        append_data(data, salary_format)
                        append_data(data, estimated_salary)
                        append_data(data, salary_min)
                        append_data(data, salary_max)
                        append_data(data, job_source)
                        append_data(data, job_type)
                        append_data(data, job_description_tags)
                        count += 1
                        total_job += 1
                        scrapped_data.append(data)

                    except Exception as e:
                        print("start up scraper loop exception => ", e)

                    finally:
                        # closes current tab
                        # driver.close()
                        # Switch back to the main page
                        driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                print("Exception in startup jobs loop => ", e)

            all_tab_handles = driver.window_handles
            for handle in all_tab_handles:
                if handle != main_tab_handle:
                    driver.switch_to.window(handle)
                    driver.close()

            # Switch back to the main tab
            driver.switch_to.window(main_tab_handle)
            print()
            try:
                wait = WebDriverWait(driver, 30)
                target_element = wait.until(
                    EC.element_to_be_clickable((By.XPATH, next_pagination_selector)))
                request_url(driver, target_element.get_attribute("href"))
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "grid"))
                )
            except Exception as e:
                print("Error in Startup Pagination => ", e)
                break

    except Exception as e:
        print("Error in Startup scrappers => ", e)

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename("start_up")
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(total_jobs=len(df), job_source="StartUp", filename=filename)
    return False, total_job


# code starts from here
def startup(link, job_type):
    total_job = 0
    try:
        driver = configure_webdriver()
        driver.maximize_window()
        flag = True
        try:
            request_url(driver, link)
            while flag:
                flag, total_job = find_jobs(driver, job_type, total_job)
                print("Fetching...")
            print(SCRAPING_ENDED)
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)

        driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)
#
# for x in links:
#     startup(x, "remote")
