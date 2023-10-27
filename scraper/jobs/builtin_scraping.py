import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs

total_job = 0

# calls url
def request_url(driver, url):
    driver.get(url)

# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))

# find's job name
def find_jobs(driver, job_type, total_job):
    try:
        scrapped_data = []
        c = 0
        time.sleep(3)
        job_links = []
        links = driver.find_elements(By.CLASS_NAME, "bounded-attribute-section")
        for link in links:
            job_links.append(link.find_element(By.TAG_NAME, "a").get_attribute('href'))

        job_details = driver.find_elements(By.CLASS_NAME, "job-bounded-responsive")
        original_window = driver.current_window_handle

        for url in job_links:
            try:
                data = []
                job_detail = job_details[c].text.split('\n')
                append_data(data, job_detail[1])
                append_data(data, job_detail[0])
                append_data(data, job_detail[2])
                driver.switch_to.new_window('tab')
                driver.get(url)
                time.sleep(4)
                try:
                    driver.find_element(By.ID, "read-more-description-toggle").click()
                    time.sleep(1)
                except Exception as e:
                    saveLogs(e)
                try:
                    address = driver.find_element(By.CLASS_NAME, "company-address").text
                except:
                    try:
                        address = driver.find_element(By.CLASS_NAME, "icon-description").text
                    except:
                        address = 'USA'
                append_data(data, address)
                job_description = driver.find_element(By.CLASS_NAME, "job-description")
                append_data(data, job_description.text)
                append_data(data, driver.current_url)
                try:
                    estimated_salary = driver.find_element(By.CLASS_NAME, "provided-salary")
                    salary = estimated_salary.text
                    if 'hour' in salary:
                        append_data(data, "hourly")
                    elif ('year' or 'annum' or 'Annually') in salary:
                        append_data(data, "yearly")
                    elif 'month' in salary:
                        append_data(data, "monthly")
                    else:
                        append_data(data, "N/A")
                    try:
                        append_data(data, k_conversion(salary.split(' A')[0]))
                    except:
                        append_data(data, "N/A")
                    try:
                        salary_min = salary.split('$')[1].split('-')[0]
                        append_data(data, k_conversion(salary_min))
                    except:
                        append_data(data, "N/A")
                    try:
                        salary_max = salary.split('$')[2].split(' A')[0]
                        append_data(data, k_conversion(salary_max))
                    except:
                        append_data(data, "N/A")
                except:
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                append_data(data, "Builtin")
                try:
                    job_type_check = driver.find_element(By.CLASS_NAME, "company-info")
                    if 'remote' in job_type_check.text.lower():
                        if 'hybrid' in job_type_check.text.lower():
                            continue
                        else:
                            append_data(data, set_job_type('Full time'))
                except Exception as e:
                    try:
                        job_type_check = driver.find_element(By.CLASS_NAME, "company-options")
                        if 'remote' in job_type_check.text.lower():
                            if 'hybrid' in job_type_check.text.lower():
                                continue
                            else:
                                append_data(data, set_job_type('Full time'))
                    except Exception as e:
                        print(e)
                        append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))

                scrapped_data.append(data)
                total_job += 1
            except Exception as e:
                saveLogs(e)
            try:
                c += 1
                driver.close()
                driver.switch_to.window(original_window)
            except Exception as e:
                saveLogs(e)

        columns_name = ["job_title", "company_name", "job_posted_date", "address", "job_description", 'job_source_url', "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.BUILTIN)
        df.to_excel(filename, index=False)

        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Builtin", filename=filename)

        try:
            next_page = driver.find_element(By.CLASS_NAME, 'pagination')
            pagination = next_page.find_elements(By.TAG_NAME, 'li')
            pagination[-1].click()
            return True, total_job
        except Exception as e:
            return False, total_job
    except Exception as e:
        saveLogs(e)
        return False, total_job

# code starts from here
def builtin(link, job_type):
    print("Builtin")
    try:
        total_job = 0
        count = 0
        driver = configure_webdriver()
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, link)
            driver.maximize_window()
            while flag:
                flag, total_job = find_jobs(driver, job_type, total_job)
            count += 1
        except Exception as e:
            saveLogs(e)

        driver.quit()
    except Exception as e:
        saveLogs(e)
