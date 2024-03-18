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
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type
from utils.helpers import saveLogs


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type):
    scrapped_data = []
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blog-img"))
        )
    except Exception as error:
        print(error)

    jobs = driver.find_elements(By.CLASS_NAME, "blog-img")
    total_job = len(jobs)
    jobs[0].click()

    iterator = 0
    while iterator < total_job:
        time.sleep(3)
        data = []
        job = driver.find_element(By.CLASS_NAME, "span9")

        if job:
            job_title = job.find_element(By.CLASS_NAME, "headline").text
            append_data(data, job_title)

            temp = job.find_element(By.CLASS_NAME, "span6").text
            temp = temp.splitlines()
            company = temp[0].split(":")
            append_data(data, company[1])

            address = temp[1].split(":")
            append_data(data, address[1])

            des = job.find_elements(By.CLASS_NAME, "job_content")
            job_description = [d for d in des][1]
            append_data(data, job_description.text)

            job_source_url = driver.current_url
            append_data(data, job_source_url)

            temp1 = job.find_element(By.CLASS_NAME, "span4").text
            temp1 = temp1.splitlines()
            job_posted_date = temp1[1].split(":")
            append_data(data, job_posted_date[1])

            salary_format = "N/A"
            append_data(data, salary_format)

            estimated_salary = "N/A"
            append_data(data, estimated_salary)

            salary_min = "N/A"
            append_data(data, salary_min)

            salary_max = "N/A"
            append_data(data, salary_max)

            job_source = ScraperNaming.RUBY_NOW
            append_data(data, job_source)

            job_type = temp1[0].split(":")
            append_data(data, set_job_type(full_time_setter(job_type[1])))

            job_description_tags = job_description.get_attribute("innerHTML")
            append_data(data, str(job_description_tags))


            scrapped_data.append(data)
            but = job.find_element(By.CLASS_NAME, "pull-right")
            but = but.find_elements(By.TAG_NAME, "a")
            but = [d for d in but][-1]
            but.click()
            iterator += 1

    columns_name = [
        "job_title",
        "company_name",
        "address",
        "job_description",
        "job_source_url",
        "job_posted_date",
        "salary_format",
        "estimated_salary",
        "salary_min",
        "salary_max",
        "job_source",
        "job_type",
        "job_description_tags",
    ]

    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.RUBY_NOW)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Ruby Now", filename=filename
    )
    return False, total_job

def full_time_setter(type):
    if type.strip().lower() == "full-time":
        return "Full Time"
    else:
        return "Contract"

# code starts from here
def rubynow(link, job_type):
    print("Ruby Now")
    # link = "https://jobs.rubynow.com/"
    # job_type = "Full Time"
    driver = configure_webdriver()
    try:
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

    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()
