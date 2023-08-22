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
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming
from utils.helpers import saveLogs


def load_all_jobs(driver):
    jobs = []
    jobs_len = len(driver.find_elements(By.CLASS_NAME, "List__item__a2c7522"))
    while True:
        try:
           show_more = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "List__showMoreBtn__cbb9f47"))
            )
        except Exception as error:
            print(error)
        show_more.click()
        time.sleep(2)
        if jobs_len == len(driver.find_elements(By.CLASS_NAME, "List__item__a2c7522")):
            break
        jobs = driver.find_elements(By.CLASS_NAME, "List__item__a2c7522")
        jobs_len = len(jobs)

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
    print(total_jobs)
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

            print(job_title)
            total_jobs =total_jobs-1
            print(total_jobs)
        

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

    import pdb
    pdb.set_trace()

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Startwire", filename=filename
    )

    return False, total_job


# code starts from here
def startwire(link, job_type):
    print("startwire")

    try:
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )

        with webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        ) as driver:
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


startwire('https://www.startwire.com/job/search?query=Engineer%20Developer%20%20Software&location_title=&radius=100&age=all', '')
