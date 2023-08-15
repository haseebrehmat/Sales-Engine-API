import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from utils.helpers import saveLogs
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming

total_job = 0

def find_jobs(driver, job_type, total_job, search_keyword, location_type):
    scrapped_data = []
    count = 0
    posted_count = 0
    # here is a logic of open 2 tabs and shifting from one to another
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    time.sleep(1)
    details_window = driver.current_window_handle
    driver.switch_to.window(original_window)
    try:
        # Here is the logic of making query
        search_div = driver.find_elements(By.NAME, "search-container")[0]
        search = search_div.find_elements(By.TAG_NAME, "input")[0]
        search.click()
        search.clear()
        search.send_keys(search_keyword)
        search = search_div.find_elements(By.TAG_NAME, "input")[1]
        search.click()
        search.clear()
        search.send_keys(location_type)
        search_div.find_elements(By.TAG_NAME, "a")[0].click()
        time.sleep(2)
        search.click()
        time.sleep(2)
        select_first_opt = search.find_element(By.XPATH,
                                               "./following-sibling::*[1]").find_elements(By.TAG_NAME, "li")[0].click()
        # here is the logic of set most recent jobs
        relevant_button = driver.find_elements(By.CLASS_NAME, "input-container")[13]
        relevant_button.click()
        relevant_button.find_elements(By.TAG_NAME, "span")[1].click()
    except:
        return False, total_job
    time.sleep(5)
    flag_count = True
    while(flag_count):
        driver.switch_to.window(original_window)
        time.sleep(10)
        jobs = driver.find_element(By.ID, "search-results").find_elements(By.TAG_NAME, "li")
        for job in jobs:
            data = []
            try:
                driver.switch_to.window(original_window)
                time.sleep(3)
                job_title = job.find_element(By.TAG_NAME, "h2").text
                job_link = job.find_elements(By.TAG_NAME, "a")[0].get_attribute('href')
                company_name = job.find_elements(By.TAG_NAME, "a")[1].text
                job_posted_date = job.find_element(By.TAG_NAME, "p").text
                if 'day ago' in job_posted_date:
                    posted_count += 1
                if posted_count > 7:
                    break
                job_source = "himalayas"
                job_source_url = job_link
                driver.switch_to.window(details_window)
                driver.get(job_link)
                time.sleep(3)
                job_description = driver.find_elements(By.CLASS_NAME, "trix-content")[0]
                job_description_tags = job_description.get_attribute('innerHTML')
                job_description = job_description.text
                main_grid = driver.find_elements(By.TAG_NAME, "section")[1].find_elements(By.CLASS_NAME, "grid")[0]
                try:
                    job_type = main_grid.find_elements(By.TAG_NAME, "div")[2].find_element(By.TAG_NAME, "p").text
                    if location_type == "United States":
                        if job_type == 'Full Time':
                            job_type = 'Full Time on Site'
                        elif job_type == 'Contractor' or job_type == 'Part Time':
                            job_type = 'Contract OnSite'
                    elif location_type == "Only 100% remote jobs":
                        if job_type == 'Full Time':
                            job_type = 'Full Time Remote'
                        elif job_type == 'Contractor' or job_type == 'Part Time':
                            job_type = 'Contract Remote'
                except:
                    job_type = "Full Time on Site"
                try:
                    salary_format = '$'
                    estimated_salary = main_grid.find_elements(By.TAG_NAME, "div")[7].find_element(By.TAG_NAME, "p").text
                    salary_min = estimated_salary.split("-")[0]
                    salary_max = estimated_salary.split("-")[1].split(" ")[0]

                except:
                    salary_format = "N/A"
                    estimated_salary = "N/A"
                    salary_max = "N/A"
                    salary_min = "N/A"
                try:
                    location = driver.find_elements(By.TAG_NAME, "main")[0].find_element(By.TAG_NAME, "header").find_elements(
                    By.TAG_NAME, "div")[0].find_element(By.CLASS_NAME, "badge-text").text
                except:
                    location = "United States"

                append_data(data, job_title)
                append_data(data, company_name)
                append_data(data, location)
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
                total_job += 1
                scrapped_data.append(data)
            except Exception as e:
                print(e)
            count += 1
        try:
            driver.switch_to.window(original_window)
            time.sleep(3)
            next_button = driver.find_element(By.CLASS_NAME, "pagination").find_elements(By.TAG_NAME, "a")[-1]
            if 'Next' in next_button.text:
                time.sleep(5)
                next_button.click()
                time.sleep(3)
            else:
                break
        except:
            flag_count = False
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.HIMALAYAS)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Himalayas", filename=filename)
    return False, total_job


def append_data(data, field):
    data.append(str(field).strip("+"))

# Create your views here.
def himalayas(link, job_type):
    print("Himalayas Scraper")
    total_job = 0
    i = 1
    while(i < 5):
        if i == 1:
            search_keyword = "Software Engineer"
            location_type = "United States"
        elif i == 2:
            search_keyword = "Software Engineer"
            location_type = "Only 100% remote jobs"
        elif i == 3:
            search_keyword = "Developer"
            location_type = "United States"
        elif i == 4:
            search_keyword = "Developer"
            location_type = "Only 100% remote jobs"
        try:
            options = webdriver.ChromeOptions()  # newly added
            options.add_argument("--headless")
            options.add_argument("window-size=1200,1100")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
            )
            with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
                driver.maximize_window()
                try:
                    flag = True
                    driver.get(link)
                    while flag:
                        flag, total_job = find_jobs(
                            driver, job_type, total_job, search_keyword, location_type)
                        print("Fetching...")
                except Exception as e:
                    print(e)
                driver.quit()
        except:
            print("Error Occurs. \n")
        i += 1