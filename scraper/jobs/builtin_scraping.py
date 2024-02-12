import time

import pandas as pd
from selenium.webdriver.common.by import By

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type, run_pia_proxy, change_pia_location
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
        time.sleep(2)
        job_links = []
        links = driver.find_elements(By.CSS_SELECTOR, "a[data-id='view-job-button']")
        for link in links:
            job_links.append(link.get_attribute('href'))

        job_details = driver.find_elements(By.CLASS_NAME, "job-bounded-responsive")
        job_det = []
        for job in job_details:
            job_det.append(job.text)
        original_window = driver.current_url

        retries  = 5
        for i, url in enumerate(job_links):
            try:
                data = []
                job_detail = job_det[i].split('\n')
                append_data(data, job_detail[1])
                append_data(data, job_detail[0])
                append_data(data, job_detail[2])
                # driver.switch_to.new_window('tab')
                driver.get(url)
                time.sleep(2)
                outer_loop_exit = False
                for retry in range(retries):
                    try:
                        driver.find_element(By.ID, "read-more-description-toggle").click()
                        # time.sleep(1)
                        break
                    except Exception as e:
                        if retry == retries:
                            saveLogs(e)
                            outer_loop_exit = True
                            break
                        error_status = change_pia_location(driver)
                        if not error_status:
                            driver.get(url)
                        else:
                            outer_loop_exit = True
                            break
                if outer_loop_exit:
                    continue
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
                        append_data(data, set_job_type('Full time', 'remote'))
                    elif 'hybrid' in job_type_check.text.lower():
                        append_data(data, set_job_type('Full time', 'hybrid'))
                    else:
                        append_data(data, set_job_type('Full time', 'onsite'))
                except Exception as e:
                    try:
                        job_type_check = driver.find_element(By.CLASS_NAME, "company-options")
                        if 'remote' in job_type_check.text.lower():
                            append_data(data, set_job_type('Full time', 'remote'))
                        elif 'hybrid' in job_type_check.text.lower():
                            append_data(data, set_job_type('Full time', 'hybrid'))
                        else:
                            append_data(data, set_job_type('Full time', 'onsite'))
                    except Exception as e:
                        print(e)
                        append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))

                scrapped_data.append(data)
                total_job += 1
            except Exception as e:
                saveLogs(e)
                print(e)

            # switch_tab(driver, c, original_window)

        columns_name = ["job_title", "company_name", "job_posted_date", "address", "job_description", 'job_source_url', "salary_format",
                        "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.BUILTIN)
        df.to_excel(filename, index=False)

        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Builtin", filename=filename)

        try:
            driver.get(original_window)
            time.sleep(2)
            next_page = driver.find_element(By.CLASS_NAME, 'pagination')
            pagination = next_page.find_elements(By.TAG_NAME, 'li')
            next_page_anchor = pagination[-1].find_element(By.TAG_NAME, 'a')
            next_page_url = next_page_anchor.get_attribute('href')
            driver.get(next_page_url)
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
        driver = configure_webdriver(block_media=True, block_elements=['css', 'img'])
        driver.maximize_window()
        run_pia_proxy(driver)
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
