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
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
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
def find_jobs(driver, scrapped_data, job_type, url=None):
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
            job.click()
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jobs-unified-top-card__job-title"))
            )
        except Exception as e:
            saveLogs(e)
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

                scrapped_data.append(data)
        except Exception as e:
            saveLogs(e)
            print(e)

    date_time = str(datetime.now())
    columns_name = ["job_title", "company_name", "address", "job_description",
                    'job_source_url', "job_posted_date", "job_source", "job_type"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(f'scraper/job_data/linkedin - {date_time}.csv', index=False)
    return True


# check if there is more jobs available or not
def data_exists(driver):
    try:
        page_exists = driver.find_elements(
            By.CLASS_NAME, "jobs-search-no-results-banner__image")
        return True if page_exists[0].text == '' else False
    except Exception as e:
        saveLogs(e)
        return True


def jobs_types(driver, url, job_type, scrapped_data):
    global total_job
    count = 0
    request_url(driver, url)  # select type from the const file
    if find_jobs(driver, scrapped_data, job_type):
        count += 25

        while find_jobs(driver, scrapped_data, job_type, "&start=" + str(count)):
            count += 25
            total_job += 25
    else:
        print(NO_JOB_RESULT)


# code starts from here
def linkedin(link, job_type):
    print("linkedin")
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
            # types = [CONTRACT_JOB_URL, FULL_TIME_JOB_URL, REMOTE_JOB_URL]
            types = [link]
            job_type = [job_type]
            try:
                # query = list(JobSourceQuery.objects.filter(job_source='linkedin').values_list("queries", flat=True))[0]
                # for c in range(len(query)):
                #     types.append(query[c]['link'])
                #     job_type.append(query[c]['job_type'])
                if logged_in:
                    count = 0
                    scrapped_data = []
                    for url in types:
                        jobs_types(driver, url, job_type[count], scrapped_data)
                        print(job_type[count], "is done")
                        count += 1
                    print(SCRAPING_ENDED)
                else:
                    print(LOGIN_FAILED)
            except Exception as e:
                print(e)
                saveLogs(e)
                print(LINK_ISSUE)
            ScraperLogs.objects.create(
                total_jobs=total_job, job_source="Linkedin")
    except Exception as e:
        saveLogs(e)
        print(e)
