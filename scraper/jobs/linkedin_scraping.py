from datetime import datetime

from scraper.constants.const import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

from scraper.models import JobSourceQuery
from scraper.models.scraper_logs import ScraperLogs
from utils.helpers import saveLogs

total_job = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# login method
def login(driver):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
    except Exception as e:
        print(e)
        saveLogs(e)
        return False

    try:
        driver.find_element(By.ID, "username").click()
        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(USERNAME)

        driver.find_element(By.ID, "password").click()
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(PASSWORD)

        driver.find_element(By.CLASS_NAME, "btn__primary--large").click()
        not_logged_in = driver.find_elements(
            By.CLASS_NAME, "form__label--error")
        if len(not_logged_in) > 0:
            return False

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "global-nav__primary-item"))
        )
        return True

    except Exception as e:
        print(e)
        saveLogs(e)
        return False


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type, url=None):
    scrapped_data = []
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "jobs-search-results__list-item"))
        )
    except:
        print("waited for jobs")

    try:
        if url is not None:
            get_url = driver.current_url
            request_url(driver, get_url + str(url))
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jobs-search-results__list-item"))
            )
    except Exception as e:
        saveLogs(e)
        return False

    time.sleep(2)
    if not data_exists(driver):
        return False

    jobs = driver.find_elements(
        By.CLASS_NAME, "jobs-search-results__list-item")

    for job in jobs:
        try:
            job.location_once_scrolled_into_view
        except Exception as e:
            print(e)

    for job in jobs:
        try:
            data = []
            job.click()

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jobs-unified-top-card__job-insight"))
            )

            job_posted_date = driver.find_elements(
                By.CLASS_NAME, "jobs-unified-top-card__posted-date")
            if job_posted_date:
                job_title = driver.find_element(
                    By.CLASS_NAME, "jobs-unified-top-card__job-title")
                append_data(data, job_title.text)
                company_name = driver.find_element(
                    By.CLASS_NAME, "jobs-unified-top-card__company-name")
                append_data(data, company_name.text)
                address = driver.find_element(
                    By.CLASS_NAME, "jobs-unified-top-card__bullet")
                append_data(data, address.text)
                job_description = driver.find_element(
                    By.CLASS_NAME, "jobs-description-content__text")
                append_data(data, job_description.text)
                job_source_url = driver.find_element(
                    By.CLASS_NAME, "jobs-unified-top-card__content--two-pane")
                url = job_source_url.find_element(By.TAG_NAME, 'a')
                append_data(data, url.get_attribute('href'))
                append_data(data, job_posted_date[0].text)
                append_data(data, "Linkedin")
                append_data(data, job_type)
                append_data(data, job_description.get_attribute('innerHTML'))

                scrapped_data.append(data)
        except Exception as e:
            print(e)

    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description",
                    'job_source_url', "job_posted_date", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = f'scraper/job_data/linkedin - {date_time}.xlsx'
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Linkedin", filename=filename)
    return True


# check if there is more jobs available or not
def data_exists(driver):
    try:
        page_exists = driver.find_elements(
            By.CLASS_NAME, "jobs-search-no-results-banner__image")
        return True if page_exists[0].text == '' else False
    except Exception as e:
        return True


def jobs_types(driver, url, job_type, total_job):
    count = 0
    request_url(driver, url)  # select type from the const file
    if find_jobs(driver, job_type):
        count += 25

        while find_jobs(driver, job_type, "&start=" + str(count)):
            count += 25
            total_job += 25
        return total_job
    else:
        print(NO_JOB_RESULT)
        return total_job


# code starts from here
def linkedin(link, job_type):
    print("linkedin")
    total_job = 0
    try:
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        # options.headless = True  # newly added
        # driver = webdriver.Chrome('/home/dev/Desktop/selenium')
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options) as driver:  # modified
            request_url(driver, LOGIN_URL)
            logged_in = login(driver)
            try:
                if logged_in:
                    total_job = jobs_types(
                        driver, link, job_type, total_job)
                    print(SCRAPING_ENDED)
                else:
                    print(LOGIN_FAILED)
            except Exception as e:
                print(e)
                saveLogs(e)
                print(LINK_ISSUE)

            driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)


