import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scraper.models import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs
from scraper.utils.helpers import configure_webdriver

total_job = 0


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def update_job_description(driver, data):
    current_url = driver.current_url
    try:
        for i in range(len(data)):
            driver.get(data[i][4])
            job_description = driver.find_elements(By.CLASS_NAME, "prose")[0]
            data[i][3] = job_description.text
            data[i][-1] = job_description.get_attribute('innerHTML')
    except Exception as e:
        saveLogs(e)
    driver.get(current_url)


# find's job name
def find_jobs(driver, job_type, total_job, link):
    try:
        request_url(driver, f'{link}')
        stop_flag = False

        scrapped_data = []

        job_section = driver.find_elements(By.TAG_NAME, "ul")[3]

        jobs = job_section.find_elements(By.TAG_NAME, "li")

        salary_format = ""

        for job in jobs:

            data = []

            if len(job.text.split("\n")) == 5:

                job_title, company_name, address, estimated_salary, job_posted_date = job.text.split("\n")

                if "k" in estimated_salary or "K" in estimated_salary:
                    salary_format = "Yearly"

                elif "year" in estimated_salary.lower():
                    salary_format = "Yearly"
                elif "hour" in estimated_salary.lower():
                    salary_format = "Hourly"
                elif "month" in estimated_salary.lower():
                    salary_format = "Monthly"

                estimated_salary = k_conversion(estimated_salary)

                estimated_salary = estimated_salary.split("-")

                min_salary, max_salary = estimated_salary.split("-")


            elif len(job.text.split("\n")) == 4:
                # Character to search for
                char_to_find = "$"

                # Check if the character exists in any string
                found = any(char_to_find in s for s in job.text.split("\n"))

                if not found:
                    job_title, company_name, address, job_posted_date = job.text.split("\n")
                    salary_format = "N/A"
                    estimated_salary = "N/A"
                    min_salary = "N/A"
                    max_salary = "N/A"

            elif len(job.text.split("\n")) == 3:
                job_title, company_name, job_posted_date = job.text.split("\n")

            job_description = ""
            job_url = job.find_element(By.TAG_NAME, "a").get_attribute("href")
            data.append(job_title)
            data.append(company_name)
            data.append(address)
            data.append(job_description)
            data.append(job_url)
            data.append(job_posted_date)
            data.append(salary_format)
            data.append(estimated_salary)
            data.append(min_salary)
            data.append(max_salary)
            data.append("Ruby On Remote")
            data.append(set_job_type("Full time remote"))
            scrapped_data.append(data)
            total_job += 1

        update_job_description(driver, scrapped_data)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                        "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                        "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.RUBY_ON_REMOTE)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(df), job_source="RubyOnRemote", filename=filename)
        index = -1
        try:
            # pagination = driver.find_elements(By.CLASS_NAME, "paging")[0].find_elements(By.TAG_NAME, 'li')
            index = driver.find_elements(By.CLASS_NAME, "next")[0].get_attribute('class').find('disabled')
            if index != -1:
                return False
            else:
                return True
        except Exception as e:
            saveLogs(e)
            return False

    except Exception as e:
        saveLogs(e)
        print(f'scrapped stopped due to: {e}')
        return False, total_job


# code starts from here
def ruby_on_remote(link, job_type):
    base_link = link

    total_job = 0

    print("RubyOnRemote")

    try:
        driver = configure_webdriver()
        driver.maximize_window()
        flag = True
        count = 0
        try:
            while flag:
                if count != 0:
                    link = f'{base_link}?page={count + 1}'
                flag = find_jobs(driver, job_type, total_job, link)
                count = count + 1
                print("Fetching...")
        except Exception as e:
            print(e)

        driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)

# link = "https://rubyonremote.com/remote-jobs-in-us/"
# job_type = "Remote"
#
# ruby_on_remote(link,job_type)

# contract_remote = "https://rubyonremote.com/contract-remote-jobs/"
# ft_remote = "https://rubyonremote.com/full-time-remote-jobs/"
