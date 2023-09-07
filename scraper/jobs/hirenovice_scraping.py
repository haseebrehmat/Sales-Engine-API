import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver

total_job = 0

def find_jobs(driver, job_type, total_job, search_keyword, location_type, remote_status):
    scrapped_data = []
    count = 0

    # here is a logic of open 2 tabs and shifting from one to another
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    time.sleep(1)
    details_window = driver.current_window_handle
    driver.switch_to.window(original_window)
    try:
        # Here is the logic of making query
        search_div = driver.find_element(By.CLASS_NAME, "search_jobs")
        search_div.location_once_scrolled_into_view
        search = search_div.find_element(By.CLASS_NAME, "search_keywords")
        search = search.find_element(By.ID, "search_keywords")
        search.click()
        search.clear()
        search.send_keys(search_keyword)

        search = search_div.find_element(By.CLASS_NAME, "search_location")
        search = search.find_element(By.ID, "search_location")
        search.click()
        search.clear()
        search.send_keys(location_type)

        if remote_status:
            search = search_div.find_element(By.CLASS_NAME, "search_remote_position")
            search = search.find_element(By.TAG_NAME, "input")
            search.click()

        search = search_div.find_element(By.CLASS_NAME, "search_submit")
        search = search.find_element(By.TAG_NAME, "input")
        search.click()
    except:
        return False, total_job
    time.sleep(5)

    for i in range(10):
        try:
            sub_div = driver.find_element(By.CLASS_NAME, "elementor-element-ef3f330")
            button = sub_div.find_element(By.CLASS_NAME, "load_more_jobs")

            # Scroll the button into view
            driver.execute_script("arguments[0].scrollIntoView();", button)

            # Wait for the button to be clickable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "load_more_jobs")))

            # Click the button
            button.click()
            time.sleep(3)  # Optional: Add a delay to allow new content to load
        except Exception as e:
            print(f"Error: {str(e)}")
            break  # Exit the loop in case of an error
    jobs = driver.find_element(By.CLASS_NAME, "job_listings").find_elements(By.CLASS_NAME, "job_listing")
    for job in jobs:
        data = []
        try:
            driver.switch_to.window(original_window)
            time.sleep(2)
            job_title = job.find_element(By.TAG_NAME, "h3").text
            company_name = job.find_element(By.CLASS_NAME, "company").text
            job_type = job.find_elements(By.CLASS_NAME, "job-type")[0].text
            if job_type == 'Full-time' or job_type == 'Full Time' or job_type == 'Permanent':
                job_type = 'Full Time Remote'
            elif (job_type == 'Part Time' or job_type == 'Temporary' or job_type == 'Contractor' or
                  job_type == 'Seasonal'):
                job_type = 'Contract Remote'
            else:
                job_type = 'Full Time Remote'
            location = "United States"
            job_source = "hirenovice"

            job_link = job.find_element(By.TAG_NAME, "a").get_attribute('href')
            driver.switch_to.window(details_window)
            driver.get(job_link)
            time.sleep(3)
            job_posted_date = (driver.find_element(By.CLASS_NAME, "single_job_listing").find_element
                               (By.CLASS_NAME, "date-posted").text)
            if 'day ago' in job_posted_date or 'days ago' in job_posted_date:
                break
            job_source_url = job_link
            estimated_salary = "N/A"
            salary_max = "N/A"
            salary_min = "N/A"
            salary_format = "N/A"
            job_description = driver.find_element(By.CLASS_NAME, "job_description")
            job_description_tags = job_description.get_attribute('innerHTML')
            job_description = job_description.text

            append_data(data, job_title)
            append_data(data, company_name)
            append_data(data, location)
            append_data(data, job_description)
            append_data(data, job_source_url)
            append_data(data, job_posted_date)
            append_data(data, salary_format)
            append_data(data, estimated_salary)
            append_data(data, salary_min)
            append_data(data, salary_max)
            append_data(data, job_source)
            append_data(data, job_type)
            append_data(data, job_description_tags)

            total_job += 1
            scrapped_data.append(data)
        except Exception as e:
            print(e)
        count += 1

    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                    "salary_format",
                    "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.HIRENOVICE)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Hirenovice", filename=filename)
    return False, total_job


def append_data(data, field):
    data.append(str(field).strip("+"))




def hirenovice(link, job_type):
    print("Hirenovice Scraper")
    total_job = 0
    i = 1
    try:
        while (i < 5):
            if i == 1:
                search_keyword = "software engineer"
                location_type = "united states"
                remote_status = False
            elif i == 2:
                search_keyword = "software engineer"
                location_type = "united states"
                remote_status = True
            elif i == 3:
                search_keyword = "developer"
                location_type = "united states"
                remote_status = False
            elif i == 4:
                search_keyword = "developer"
                location_type = "united states"
                remote_status = True
            try:
                driver = configure_webdriver()
                driver.maximize_window()
                try:
                    flag = True
                    driver.get(link)
                    while flag:
                        flag, total_job = find_jobs(
                            driver, job_type, total_job, search_keyword, location_type, remote_status)
                        print("Fetching...")
                except Exception as e:
                    print(e)
                driver.quit()
            except:
                print("Error Occurs. \n")
            i += 1
    except Exception as e:
        print(e)