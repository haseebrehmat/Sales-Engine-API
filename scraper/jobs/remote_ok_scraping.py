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
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, remove_emojis
from utils.helpers import saveLogs


def load_jobs(driver):
    previous_len = len(driver.find_elements(
        By.CLASS_NAME, "company_and_position"))
    while True:
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        elements = driver.find_elements(By.CLASS_NAME, "company_and_position")
        if previous_len == len(elements):
            break
        previous_len = len(elements)


def get_job_urls(driver):
    load_jobs(driver)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "company_and_position"))
        )
    except Exception as error:
        print(error)
    job_urls = driver.find_elements(By.CLASS_NAME, "company_and_position")
    links = []
    for job_url in job_urls:
        link = job_url.find_element(By.TAG_NAME, "a")
        link.get_attribute("href")
        links.append(link.get_attribute("href"))
    return links

# calls url


def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def find_jobs(driver, job_type):
    scrapped_data = []

    links = get_job_urls(driver)
    
    total_job = len(links)
    links.pop(0)
    for link in links:
        data = []
        if link:
            try:
                driver.get(link)
                id = link.split("-")[-1]
                time.sleep(5)
                job = driver.find_element(By.CLASS_NAME, f"job-{id}")
                job_desc = driver.find_element(By.CLASS_NAME, "expandContents")
            except:
                print("error in scrapping")

            temp = job.find_element(By.CLASS_NAME, "company_and_position").text
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

            job_source = ScraperNaming.Remote_Ok
            append_data(data, job_source)

            job_type = "remote"
            append_data(data, job_type)

            job_description_tags = job_desc.get_attribute("innerHTML")
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
    filename = generate_scraper_filename(ScraperNaming.Remote_Ok)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Remote ok", filename=filename
    )

    return False, total_job


# code starts from here
def remoteok(link, job_type):
    print("Remote Ok")

    try:
        options = webdriver.ChromeOptions()  # newly added
        # options.add_argument("--headless")
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


remoteok('https://remoteok.com/remote-api+engineer-jobs?order_by=date','full time remote')
