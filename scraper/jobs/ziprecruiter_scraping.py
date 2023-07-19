from datetime import datetime
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming
from utils.helpers import saveLogs


def ziprecruiter_scraping(links, job_type):
    print("Zip Recruiter")
    # date_time = str(datetime.now())
    c = 0
    options = webdriver.ChromeOptions()  # newly added
    options.add_argument("--headless")
    options.add_argument("window-size=1200,1100")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    )
    # options.headless = True  # newly added
    # with webdriver.Chrome('/home/dev/Desktop/selenium') as driver:
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:  # modified
        original_window = driver.current_window_handle
        driver.switch_to.new_window('tab')
        details_window = driver.current_window_handle
        driver.switch_to.window(original_window)
        driver.get(links)

        while True:
            try:
                next_btn = driver.find_elements(By.CLASS_NAME, 'load_more')
                next_btn[0].location_once_scrolled_into_view
                if len(next_btn) > 0:
                    next_btn[0].click()
                else:
                    break
            except:
                break
            time.sleep(5)

        all_data = []
        driver.switch_to.window(original_window)
        try:
            job_search = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "tiles_wrapper"))
            )
        except Exception as e:
            print("Hello")

        for job in job_search.find_elements(By.TAG_NAME, 'article'):
            driver.switch_to.window(original_window)

            job_detail = {'job_title': job.find_element(By.CLASS_NAME, 'title').text,
                            'company_name': job.find_element(By.CLASS_NAME, 'company_name').text,
                            'job_source': 'Ziprecruiter',
                            'address': job.find_element(By.CLASS_NAME, 'company_location').text,
                            'job_type': job_type,
                            'job_source_url': job.find_element(By.TAG_NAME, 'a').get_attribute('href')
                            }

            if 'https://www.ziprecruiter.com/k' in job_detail['job_source_url']:
                driver.switch_to.window(details_window)
                driver.get(job_detail['job_source_url'])
                job_data = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='job_more_section']"))
                )

                job_detail['job_description'] = driver.find_element(
                    By.CLASS_NAME, 'job_description').text

                try:
                    job_detail['estimated_salary'] = driver.find_element(
                        By.CLASS_NAME, 't_compensation').text.split(' p')[0]
                    if '$' in job_detail['estimated_salary']:
                        job_detail['salary_format'] = '$'
                    else:
                        job_detail['salary_format'] = 'N/A'
                    try:
                        job_detail['salary_min'] = job_detail['estimated_salary'].split(' to ')[0]
                    except:
                        job_detail['salary_min'] = 'N/A'
                    try:
                        job_detail['salary_max'] = job_detail['estimated_salary'].split(' to ')[1]
                    except:
                        job_detail['salary_max'] = 'N/A'

                except:
                    job_detail['estimated_salary'] = "N/A"
                    job_detail['salary_format'] = "N/A"
                    job_detail['salary_min'] = "N/A"
                    job_detail['salary_max'] = "N/A"

                job_detail['job_description_tags'] = driver.find_element(
                    By.CLASS_NAME, 'job_description').get_attribute('innerHTML')

                for single_job in job_data.find_elements(By.XPATH, "//p[@class='job_more']"):
                    if 'Posted date:' in single_job.text:
                        job_detail['job_posted_date'] = single_job.text
            else:
                job_detail['job_description'] = "N/A"
                job_detail['estimated_salary'] = "N/A"
                job_detail['salary_format'] = "N/A"
                job_detail['salary_min'] = "N/A"
                job_detail['salary_max'] = "N/A"
                job_detail['job_description_tags'] = "N/A"
                job_detail['job_posted_date'] = 'Today'

            all_data.append(job_detail)
        driver.switch_to.window(original_window)

        df = pd.DataFrame.from_dict(all_data)
        df['job_description'] = df['job_description'].str.replace(
            '<.*?>', '', regex=True)
        df['job_posted_date'] = df['job_posted_date'].str.replace(
            'Posted date: ', '')
        filename = generate_scraper_filename(ScraperNaming.ZIP_RECRUITER)
        df.to_excel(
            filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(
            df), job_source="Zip Recruiter", filename=filename)
        c += 1
        driver.quit()
        print("SCRAPING_ENDED")
