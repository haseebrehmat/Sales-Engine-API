from job_scraper.constants.const import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time


# calls url
def request_url(driver, url):
    driver.get(url)


# login method
def login(driver):
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    driver.find_element(By.ID, "username").click()
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(USERNAME)

    driver.find_element(By.ID, "password").click()
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(PASSWORD)

    driver.find_element(By.CLASS_NAME, "btn__primary--large").click()
    not_logged_in = driver.find_elements(By.CLASS_NAME, "form__label--error")
    if len(not_logged_in) > 0:
        return False

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "global-nav__primary-item"))
    )
    return True


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, scrapped_data, job_type, url=None):
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results__list-item"))
    )
    if url is not None:
        get_url = driver.current_url
        request_url(driver, get_url + str(url))
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results__list-item"))
        )

    time.sleep(2)
    if not data_exists(driver):
        return False

    jobs = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")

    for job in jobs:
        job.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-unified-top-card__job-title"))
        )

    for job in jobs:
        data = []
        job.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-unified-top-card__job-insight"))
        )

        job_posted_date = driver.find_elements(By.CLASS_NAME, "jobs-unified-top-card__posted-date")
        if job_posted_date:
            job_title = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__job-title")
            append_data(data, job_title.text)
            company_name = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__company-name")
            append_data(data, company_name.text)
            address = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__bullet")
            append_data(data, address.text)
            job_description = driver.find_element(By.CLASS_NAME, "jobs-description-content__text")
            append_data(data, job_description.text)
            job_source_url = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__content--two-pane")
            url = job_source_url.find_element(By.TAG_NAME, 'a')
            append_data(data, url.get_attribute('href'))
            append_data(data, job_posted_date[0].text)
            append_data(data, "Linkedin")
            append_data(data, job_type)

            scrapped_data.append(data)

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "job_source", "job_type"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(LINKEDIN_CSV, index=False)
    return True


# check if there is more jobs available or not
def data_exists(driver):
    page_exists = driver.find_elements(By.CLASS_NAME, "jobs-search-no-results-banner__image")
    return True if len(page_exists) == 0 else False


def jobs_types(driver, url, job_type):
    scrapped_data = []
    count = 0
    request_url(driver, url)  # select type from the const file
    if find_jobs(driver, scrapped_data, job_type):
        count += 25

        while (True):
            if find_jobs(driver, scrapped_data, job_type, "&start=" + str(count)):
                count += 25
            else:
                print(SCRAPING_ENDED)
                break
    else:
        print(NO_JOB_RESULT)


# code starts from here
def linkedin():
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
        request_url(driver, LOGIN_URL)
        logged_in = login(driver)
        types = [CONTRACT_JOB_URL, FULL_TIME_JOB_URL, REMOTE_JOB_URL]
        job_type = ["Contract", "Full Time on Site", "Full Time Remote"]
        if logged_in:
            for url in types:
                jobs_types(driver, url, job_type[count])
                count = count + 1
        else:
            print(LOGIN_FAILED)


# linkedin()
