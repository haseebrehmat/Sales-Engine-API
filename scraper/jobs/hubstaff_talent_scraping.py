import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import configure_webdriver, generate_scraper_filename, ScraperNaming, set_job_type
from utils.helpers import saveLogs


def get_all_jobs_urls(driver):
    jobs = driver.find_elements(By.CLASS_NAME, "search-result")
    links = [job.find_element(By.TAG_NAME, "a").get_attribute("href")
             for job in jobs]
    while True:
        try:
            pagination = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "pagination-container"))
            )
            show_more = WebDriverWait(pagination, 30).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "pull-right"))
            )

            show_more.click()
            time.sleep(5)
            new_jobs = driver.find_elements(By.CLASS_NAME, "search-result")
            new_links = [job.find_element(By.TAG_NAME, "a").get_attribute("href")
                         for job in new_jobs]
            links = [*links, *new_links]
        except Exception as e:
            print("Loaded all jobs")
            break
    return links


def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def find_jobs(driver, job_type):
    scrapped_data = []
    urls = get_all_jobs_urls(driver)
    total_jobs = len(urls)
    print('total Scrapped jobs :', total_jobs)
    for url in urls:
        data = []
        if url:
            try:
                job_source_url = url
                driver.get(job_source_url)
                job_details = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "panel")))

                temp = job_details.find_element(
                    By.CLASS_NAME, "name")

                temp1 = temp.find_element(
                    By.CLASS_NAME, "valign-middle")
                job_title = temp1.text
                append_data(data, job_title)

                temp2 = job_details.find_element(
                    By.CLASS_NAME, "job-company")

                company_name = temp2.find_element(
                    By.TAG_NAME, "a").text
                append_data(data, company_name)

                address = temp2.find_elements(
                    By.TAG_NAME, "span")[0].text.split(' ')
                address.pop(0)
                address = ''.join(address)
                append_data(data, address)

                append_data(data, job_source_url)

                job_desc = job_details.find_element(
                    By.CLASS_NAME, "job-description")
                job_description = job_desc.text
                job_description_tags = job_desc.get_attribute("innerHTML")
                append_data(data, job_description)

                job_posted_date = temp2.find_elements(
                    By.TAG_NAME, "span")[2].text
                append_data(data, job_posted_date)

                salary_format = "hourly"
                append_data(data, salary_format)

                salary_min = "N/A"
                append_data(data, salary_min)

                salary_max = "N/A"
                append_data(data, salary_max)

                estimated_salary = job_details.find_elements(By.CLASS_NAME,'job-sidebar')[0].text.splitlines()[0]
                append_data(data, estimated_salary)

                job_source = ScraperNaming.HUBSTAFF_TALENT
                append_data(data, job_source)

                job_type = temp.find_element(
                    By.CLASS_NAME, "label").text
                append_data(data, set_job_type(job_type))

                append_data(data, str(job_description_tags))

            except Exception as e:
                print("error in scrapping", e)
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
    filename = generate_scraper_filename(ScraperNaming.HUBSTAFF_TALENT)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="hubstaff talent", filename=filename
    )

    return False, total_jobs


# code starts from here
def hubstaff_talent(link, job_type):
    print("hubstaff_talent")
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


# hubstaff_talent('https://hubstafftalent.net/search/jobs?search%5Bkeywords%5D=dev&page=1&search%5Btype%5D=&search%5Blast_slider%5D=&search%5Bjob_type%5D%5B0%5D=1&search%5Bjob_type%5D%5B1%5D=1&search%5Bnewer_than%5D=Mon%2C+Sep+18+2023&search%5Bnewer_than%5D=Mon+Sep+18+2023+00%3A00%3A00+GMT%2B0500&search%5Bpayrate_start%5D=1&search%5Bpayrate_end%5D=100%2B&search%5Bpayrate_null%5D=0&search%5Bpayrate_null%5D=1&search%5Bbudget_start%5D=1&search%5Bbudget_end%5D=100000%2B&search%5Bbudget_null%5D=0&search%5Bbudget_null%5D=1&search%5Bexperience_level%5D=-1&search%5Bcountries%5D%5B%5D=&search%5Blanguages%5D%5B%5D=&search%5Bsort_by%5D=relevance',
#                 'job_type')
