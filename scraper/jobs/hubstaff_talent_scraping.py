import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import configure_webdriver, generate_scraper_filename, ScraperNaming
from utils.helpers import saveLogs


def load_all_jobs(driver):
    jobs = driver.find_elements(By.CLASS_NAME, "search-result")
    url = jobs[0].find_element(By.TAG_NAME, "a")
    print(url)
    job_source_url = url.get_attribute("href")
    print(job_source_url)
    while True:
        try:
            pagination = driver.find_element(
                By.CLASS_NAME, "pagination-container")
            show_more = WebDriverWait(pagination, 30).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "pull-right"))
            )

            show_more.click()
        except Exception as error:
            print("Loaded all jobs")
            break

        jobs.append(driver.find_elements(By.CLASS_NAME, "search-result"))
        print(len(jobs))

    jobs = driver.find_elements(By.CLASS_NAME, "List__item__a2c7522")
    return jobs


def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def find_jobs(driver, job_type):
    scrapped_data = []
    jobs = load_all_jobs(driver)
    total_jobs = len(jobs)
    print('total jobs :', total_jobs)
    for job in jobs:
        data = []
        if job:
            try:
                url = job.find_element(By.TAG_NAME, "a")
                job_source_url = url.get_attribute("href")
                original_window = driver.current_window_handle
                driver.switch_to.new_window('tab')
                driver.get(job_source_url)
                job_desc = driver.find_element(
                    By.CLASS_NAME, "HappyTemplate__body__fcf8deb")
                job_description = job_desc.text
                job_description_tags = job_desc.get_attribute("innerHTML")
                time.sleep(1)
                driver.close()
                driver.switch_to.window(original_window)
            except:
                print("error in scrapping")

            temp = job.text
            temp = temp.splitlines()

            job_title = temp[0]
            append_data(data, job_title)

            company_name = temp[1]
            append_data(data, company_name)

            address = temp[2]
            append_data(data, address)

            append_data(data, job_source_url)

            append_data(data, job_description)

            job_posted_date = temp[-2]
            append_data(data, job_posted_date)

            salary_format = "N/A"
            append_data(data, salary_format)

            salary_min = "N/A"
            append_data(data, salary_min)

            salary_max = "N/A"
            append_data(data, salary_max)

            estimated_salary = "N/A"
            append_data(data, estimated_salary)

            job_source = ScraperNaming.STARTWIRE
            append_data(data, job_source)

            job_type = "remote"
            append_data(data, job_type)

            append_data(data, str(job_description_tags))

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
    filename = generate_scraper_filename(ScraperNaming.STARTWIRE)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Startwire", filename=filename
    )

    return False, total_jobs


# code starts from here
def hubstaff_talent(link, job_type):
    print("hubstaff_talent")

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


hubstaff_talent('https://talent.hubstaff.com/search/jobs?search%5Bkeywords%5D=&page=1&search%5Btype%5D=&search%5Blast_slider%5D=&search%5Bjob_type%5D%5B0%5D=1&search%5Bjob_type%5D%5B1%5D=1&search%5Bnewer_than%5D=Sun%2C+Sep+10+2023&search%5Bnewer_than%5D=Sun+Sep+10+2023+00%3A00%3A00+GMT%2B0500&search%5Bpayrate_start%5D=1&search%5Bpayrate_end%5D=100%2B&search%5Bpayrate_null%5D=0&search%5Bpayrate_null%5D=1&search%5Bbudget_start%5D=1&search%5Bbudget_end%5D=100000%2B&search%5Bbudget_null%5D=0&search%5Bbudget_null%5D=1&search%5Bexperience_level%5D=-1&search%5Bcountries%5D%5B%5D=&search%5Blanguages%5D%5B%5D=&search%5Bsort_by%5D=relevance', 'job_type')
