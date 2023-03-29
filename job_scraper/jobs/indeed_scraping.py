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


# find's job name
def find_jobs(driver, scrapped_data, job_type):
    c = 0
    time.sleep(3)
    jobs = driver.find_elements(By.CLASS_NAME, "slider_container")
    company_name = driver.find_elements(By.CLASS_NAME, "companyName")

    for job in jobs:
        data = []
        time.sleep(1)
        job.click()
        time.sleep(3)

        job_title = driver.find_element(By.CLASS_NAME, "jobsearch-JobInfoHeader-title")
        append_data(data, job_title.text.replace('- job post', ''))
        # import pdb
        # pdb.set_trace()
        append_data(data, company_name[c].text)
        address = driver.find_element(By.CLASS_NAME, "css-6z8o9s")
        append_data(data, address.text.replace('•Remote', ''))
        job_description = driver.find_element(By.CLASS_NAME, "jobsearch-jobDescriptionText")
        append_data(data, job_description.text)
        append_data(data, driver.current_url)
        job_posted_date = driver.find_elements(By.CLASS_NAME, "css-659xjq")
        if len(job_posted_date) > 0:
            append_data(data, job_posted_date[0].text)
        else:
            append_data(data, 'Posted Today')
        append_data(data, "Indeed")
        append_data(data, job_type)

        scrapped_data.append(data)
        c += 1

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "job_source", "job_type"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(INDEED_CSV, index=False)

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
def indeed():
    count = 0
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
        types = [INDEED_CONTRACT_RESULTS, INDEED_FULL_RESULTS, INDEED_REMOTE_RESULTS]
        job_type = ["Contract", "Full Time on Site", "Full Time Remote"]
        for url in types:
            scrapped_data = []
            request_url(driver, url)
            driver.maximize_window()
            while find_jobs(driver, scrapped_data, job_type[count]):
                print("Fetching...")
            count = count + 1
    print(SCRAPING_ENDED)
