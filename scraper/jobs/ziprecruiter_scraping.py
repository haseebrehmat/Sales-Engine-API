from datetime import datetime

from scraper.constants.const import ZIP_RECRUITER_CSV
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime

from scraper.constants.const import *
from scraper.models import JobSourceQuery
from scraper.models.scraper_logs import ScraperLogs
from utils.helpers import saveLogs


links = [
    'https://www.ziprecruiter.com/candidate/search?search=Developer&location=USA&refine_by_location_type=no_remote&radius=100&days=1&refine_by_salary=&refine_by_tags=employment_type%3Afull_time&refine_by_title=&refine_by_org_name=',
    'https://www.ziprecruiter.com/candidate/search?search=Developer&location=USA&refine_by_location_type=&radius=100&days=1&refine_by_salary=&refine_by_tags=employment_type%3Acontract&refine_by_title=&refine_by_org_name=',
    'https://www.ziprecruiter.com/candidate/search?search=Developer&location=USA&refine_by_location_type=only_remote&radius=100&days=1&refine_by_salary=&refine_by_tags=employment_type%3Afull_time&refine_by_title=&refine_by_org_name=',
]

job_type = ["Contract", "Full Time on Site", "Full Time Remote"]


def ziprecruiter_scraping():
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
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options) as driver:  # modified
            original_window = driver.current_window_handle
            driver.switch_to.new_window('tab')
            details_window = driver.current_window_handle
            all_data = []
            for i in links:
                driver.switch_to.window(original_window)
                next_link = i
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
                    df.to_csv(
                        f'scraper/job_data/ziprecruiter - {date_time}.csv', index=False)

            c += 1
        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Zip Recruiter")

        driver.close()
        print("SCRAPING_ENDED")

    except Exception as e:
        saveLogs(e)
        print(LINK_ISSUE)
