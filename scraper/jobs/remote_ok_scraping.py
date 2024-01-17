from datetime import timedelta, datetime
from django.utils import timezone
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
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, remove_emojis, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs


def load_jobs(driver):
    previous_len = len(driver.find_elements(
        By.CLASS_NAME, "company_and_position"))
    count = 0
    while True:
        if count == 5:
            break
        count += 1
        time.sleep(3)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        elements = driver.find_elements(By.CLASS_NAME, "company_and_position")
        if previous_len == len(elements):
            break
        previous_len = len(elements)


def get_job_urls(driver):
    load_jobs(driver)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "tr[data-slug][data-id]"))
        )
    except Exception as error:
        print(error)
    job_urls = driver.find_elements(By.CSS_SELECTOR, "tr[data-slug][data-id]")
    links = []
    for job_url in job_urls:
        try:
            if (check_if_job_week_ago(job_url)):
                link = job_url.get_attribute("data-href")
                links.append(link)
        except Exception as e:
            print(e)
    return links

def check_if_job_week_ago(job):
    week_ago = False
    try:
        date_elm = job.find_element(By.TAG_NAME, "time")
        date_str = date_elm.get_attribute("datetime")
        date_obj = datetime.fromisoformat(date_str).replace(tzinfo=timezone.get_current_timezone())
        current_date = datetime.now(tz=timezone.get_current_timezone())
        one_week_ago_date = current_date - timedelta(days=7)
        if date_obj >= one_week_ago_date:
            week_ago = True
    except Exception as e:
        print(e)
    return week_ago

# calls url


def is_convertible_to_number(s):
    if isinstance(s, str):
        try:
            int(s)
            return True
        except ValueError:
            return False
    return False


def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def find_jobs(driver, job_type):
    scrapped_data = []

    links = get_job_urls(driver)
    total_job = len(links)
    original_window = driver.current_window_handle
    for link in links:
        data = []
        if link:
            try:
                driver.switch_to.new_window('tab')
                driver.get("https://remoteok.com" + link)
                time.sleep(5)
                id = link.split("-")[-1]
                if is_convertible_to_number(id):
                    id = int(id)
                    job = WebDriverWait(driver, 40).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, f"job-{id}")))
                    job_desc = WebDriverWait(driver, 40).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "expandContents")))

                    temp = job.find_element(
                        By.CLASS_NAME, "company_and_position").text
                    temp = temp.splitlines()
                    job_title = remove_emojis(temp[0])
                    append_data(data, job_title)

                    company_name = remove_emojis(temp[1])
                    append_data(data, company_name)

                    address = 'Remote'
                    append_data(data, address)

                    job_source_url = link
                    append_data(data, job_source_url)

                    job_description = job_desc.text
                    append_data(data, job_description)

                    temp1 = job.find_element(By.CLASS_NAME, "time").text
                    job_posted_date = temp1
                    append_data(data, job_posted_date)

                    salary_format = "yearly"
                    append_data(data, salary_format)

                    temp2 = temp[-1].split(" ")
                    if len(temp2[-3]) >= 4 and temp2[-3][0] == "$":
                        salary_min = remove_emojis(temp2[-3])
                    else:
                        salary_min = "N/A"
                    append_data(data, salary_min)

                    if len(temp2[-1]) >= 4 and temp2[-1][0] == "$":
                        salary_max = remove_emojis(temp2[-1])
                    else:
                        salary_max = "N/A"
                    append_data(data, salary_max)

                    if salary_max == "N/A" or salary_min == "N/A":
                        estimated_salary = "N/A"
                    else:
                        estimated_salary = f"{salary_min}-{salary_max}"
                    append_data(data, estimated_salary)

                    job_source = ScraperNaming.REMOTE_OK
                    append_data(data, job_source)

                    job_type = "remote"
                    append_data(data, set_job_type(job_type))

                    job_description_tags = job_desc.get_attribute("innerHTML")
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
    filename = generate_scraper_filename(ScraperNaming.REMOTE_OK)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Remote ok", filename=filename
    )
    return False, total_job


# code starts from here
def remoteok(link, job_type):
    print("Remote Ok")

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
