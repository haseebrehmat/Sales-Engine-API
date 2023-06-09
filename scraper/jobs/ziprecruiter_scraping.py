from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from utils.helpers import saveLogs


def ziprecruiter_scraping(links, job_type):
    print("Zip Recruiter")
    try:
        date_time = str(datetime.now())
        c = 0
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        # options.headless = True  # newly added
        with webdriver.Chrome('/home/dev/Desktop/selenium') as driver:
        # with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
        #                       options=options) as driver:  # modified
            original_window = driver.current_window_handle
            driver.switch_to.new_window('tab')
            details_window = driver.current_window_handle
            all_data = []
            driver.switch_to.window(original_window)
            next_link = links
            while 'candidate' in next_link:
                driver.switch_to.window(original_window)
                driver.get(next_link)
                try:
                    job_search = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@data-type='job_results']"))
                    )
                except Exception as e:
                    saveLogs(e)
                    continue

                for job in job_search.find_elements(By.TAG_NAME, 'article'):
                    driver.switch_to.window(original_window)
                    job_detail = {'job_title': job.get_attribute('data-job-title'),
                                  'company_name': job.get_attribute('data-company-name'),
                                  'job_source': 'Ziprecruiter',
                                  'address': job.get_attribute('data-location'),
                                  'job_type': job.find_element(By.XPATH,
                                                               "//section[@class='perks_item perks_type']").text,
                                  'job_type': job_type[c],
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
                            By.CLASS_NAME, 'jobDescriptionSection').text

                        for single_job in job_data.find_elements(By.XPATH, "//p[@class='job_more']"):
                            if 'Posted date:' in single_job.text:
                                job_detail['job_posted_date'] = single_job.text
                    else:
                        job_detail['job_posted_date'] = 'Today'

                    all_data.append(job_detail)
                driver.switch_to.window(original_window)
                next_link = 'https://www.ziprecruiter.com' + \
                            job_search.get_attribute('data-next-url')

                df = pd.DataFrame.from_dict(all_data)
                df['job_description'] = df['job_description'].str.replace(
                    '<.*?>', '', regex=True)
                df['job_posted_date'] = df['job_posted_date'].str.replace(
                    'Posted date: ', '')
                df['job_type'] = df['job_type'].str.replace('Type\n', '')
                filename = f'scraper/job_data/ziprecruiter - {date_time}.csv'
                df.to_csv(
                    filename, index=False)
                ScraperLogs.objects.create(total_jobs=len(
                    df), job_source="Zip Recruiter", filename=filename)
            c += 1

        driver.close()
        print("SCRAPING_ENDED")

    except Exception as e:
        saveLogs(e)
        print(LINK_ISSUE)
