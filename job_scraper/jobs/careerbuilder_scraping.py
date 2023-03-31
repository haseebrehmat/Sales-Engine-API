from datetime import datetime
from job_scraper.constants.const import *
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# check if there is more jobs available or not
def data_exists(driver):
    finished = "display: none;"
    page_exists = driver.find_element(By.CLASS_NAME, "btn-clear-blue")
    display = page_exists.get_attribute('style')
    return False if finished in display else True


def find_jobs(driver, scrapped_data, job_type):
    count = 0
    jobs = driver.find_elements(By.CLASS_NAME, "data-results-content-parent")

    for job in jobs:
        try:
            data = []
            job.click()
            time.sleep(3)

            job_title = driver.find_element(By.CLASS_NAME, "jdp_title_header")
            append_data(data, job_title.text)
            c_name = driver.find_elements(By.CLASS_NAME, "data-display-header_info-content")
            company = c_name[0].find_elements(By.TAG_NAME, "span")
            append_data(data, company[0].text)
            append_data(data, company[1].text)
            job_description = driver.find_element(By.CLASS_NAME, "jdp-left-content")
            append_data(data, job_description.text)
            append_data(data, driver.current_url)
            job_posted_date = driver.find_elements(By.CLASS_NAME, "data-results-publish-time")
            append_data(data, job_posted_date[count].text)
            append_data(data, "Careerbuilder")
            append_data(data, job_type)
            scrapped_data.append(data)

        except Exception as e:
            print(e)
        count += 1

    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "job_source", "job_type"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(f'job_scraper/job_data/career_builder - {date_time}.csv', index=False)


# find's job name
def load_jobs(driver):
    time.sleep(2)

    if not data_exists(driver):
        return False

    next_page = driver.find_element(By.CLASS_NAME, "btn-clear-blue")
    next_page.click()
    time.sleep(2)

    return True


# code starts from here
def career_builder():
    count = 0
    scrapped_data = []
    options = webdriver.ChromeOptions()  # newly added
    options.add_argument("--headless")
    options.add_argument("window-size=1200,1100")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    )
    # options.headless = True  # newly added
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                          options=options) as driver:  # modified
        driver.maximize_window()
        types = [CAREERBUILDER_CONTRACT_RESULTS, CAREERBUILDER_FULL_RESULTS, CAREERBUILDER_REMOTE_RESULTS]
        job_type = ["Contract", "Full Time on Site", "Full Time Remote"]
        for url in types:
            request_url(driver, url)
            while load_jobs(driver):
                print("Loading...")

            find_jobs(driver, scrapped_data, job_type[count])
            count = count + 1

    print(SCRAPING_ENDED)
