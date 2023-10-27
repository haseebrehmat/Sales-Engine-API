import math
import re
import time
import traceback
from datetime import datetime
from typing import List

import pandas as pd
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver
from utils.helpers import saveLogs


class WeWorkRemotelyScraper:
    def __init__(self, driver, url) -> None:
        self.driver: WebDriver = driver
        self.url: str = url
        self.scraped_jobs: List[dict] = []
        self.job: dict = {}
        self.errs: List[dict] = []

    @classmethod
    def call(cls, url):
        print("Running We Work Remotely...")
        try:
            driver: WebDriver = configure_webdriver(True)
            driver.maximize_window()
            wwr_scraper: cls.__class__ = cls(driver=driver, url=url)
            wwr_scraper.find_jobs()
        except Exception as e:
            print(e)
            saveLogs(e)
        print("Done We Work Remotely...")

    def request_page(self) -> None:
        self.driver.get(self.url)

    def handle_exception(self, exception: Exception or str) -> None:
        traceback.format_exc()
        traceback_data = traceback.extract_tb(exception.__traceback__)
        if traceback_data and traceback_data[0]:
            self.errs.append({
                'scraper': 'weworkremotely',
                'file_path': traceback_data[0].filename or "",
                'line_number': traceback_data[0].lineno or "",
                'error_line': traceback_data[0].line or "",
                'from_function': traceback_data[0].name or ""
            })

    def get_element(self, locator: str, parent: WebElement = None, selector: str = 'class',
                    alls: bool = False) -> WebElement or List[WebElement] or None:
        try:
            by: str = By.CLASS_NAME
            if selector == 'css':
                by: str = By.CSS_SELECTOR
            if selector == 'xpath':
                by: str = By.XPATH
            if selector == 'tag':
                by: str = By.TAG_NAME
            if selector == 'name':
                by: str = By.NAME  # For Input fields
            wait: WebDriverWait = WebDriverWait(parent or self.driver, 10)
            ec: EC = EC.presence_of_all_elements_located((by, locator)) if alls else EC.presence_of_element_located(
                (by, locator))
            return wait.until(ec)
        except WebDriverException as e:
            self.handle_exception(e)
            return None

    def home_page_loaded(self) -> bool:
        loaded: bool = False
        for retry in range(1, 6):
            try:
                self.request_page()
                homepage_element: WebElement = self.get_element(locator='listing_column')
                if not homepage_element:
                    time.sleep(3)
                main_element: list[WebElement] = self.driver.find_elements(By.CLASS_NAME, 'listing_column')
                if main_element:
                    loaded = True
                    break
            except WebDriverException as e:
                if retry < 5:
                    print(f"Retry {retry}/{5} due to: {e}")
                else:
                    self.handle_exception(e)
                    self.driver.quit()
                    break
        return loaded

    def extract_links(self) -> List[str]:
        job_links: list[str] = []
        if self.home_page_loaded():
            time.sleep(1)
            jobs_list: list[WebElement] = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'section.jobs ul li:not(.view-all)')
                )
            )
            for item in jobs_list:
                anchor_elements: list[WebElement] = WebDriverWait(item, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
                )
                if anchor_elements and anchor_elements[1]:
                    job_links.append(anchor_elements[1].get_attribute('href'))
        return job_links

    def extract_salary(self, salary: str) -> None:
        pattern = r"\$(?P<min>[0-9,]+)(?:\s*-\s*\$(?P<max>[0-9,]+))?(\s+OR\s+MORE)?\s+(?P<format>[A-Z]+)"
        match = re.search(pattern, salary)
        if match:
            min_salary = match.group("min") or ""
            max_salary = match.group("max") or min_salary
            unit = match.group("format") or "USD"
            currency_format = "yearly" if int(max_salary.replace(',', '')) > 1000 else "monthly"
            self.job['salary_min']: str = f"{min_salary}"
            self.job['salary_max']: str = f"{max_salary}"
            self.job['salary_format']: str = currency_format
            self.job['estimated_salary']: str = f"{min_salary} - {max_salary} {unit}"
        else:
            self.job['salary_min']: str = "N/A"
            self.job['salary_max']: str = "N/A"
            self.job['salary_format']: str = "N/A"
            self.job['estimated_salary']: str = "N/A"

    def get_job_type(self, job_type: str) -> None:
        default_type: str = 'full time remote'
        if job_type == 'FULL-TIME':
            default_type: str = 'full time remote'
        if job_type == 'CONTRACT':
            default_type: str = 'contract remote'
        self.job['job_type']: str = default_type

    @staticmethod
    def parse_posted_date(datetime_str: str) -> str:
        pattern = r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)$'
        match = re.match(pattern, datetime_str)
        if match:
            datetime_str = match.group(1)
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
            current_time = datetime.utcnow()
            time_difference = (current_time.timestamp() - datetime_obj.timestamp())
            days_difference = math.ceil(time_difference / 86400)
            seconds_difference = int(time_difference % 86400)
            hours = seconds_difference // 36000
            minutes = (seconds_difference % 3600) // 60
            if days_difference == 0 and hours == 0:
                result = f"{minutes} minutes ago"
            elif days_difference == 0:
                result = f"{hours} hours ago"
            else:
                result = f"{days_difference} days ago"
        else:
            result = datetime_str
        return result

    def extract_values_from_header(self, header: WebElement or None) -> None:
        try:
            element: WebElement or List[WebElement] or None
            if header:
                # Job Posted Date
                element: WebElement = self.get_element(locator='.listing-header-container time', selector='css',
                                                       parent=header)
                self.job['job_posted_date']: str = self.parse_posted_date(element.get_attribute('datetime'))
                # Job Title
                element: WebElement = self.get_element(locator='.listing-header-container h1', selector='css',
                                                       parent=header)
                self.job['job_title']: str = element.text if element else "N/A"
                # Salary Details
                element: list[WebElement] = self.get_element(selector='css', locator='a span.listing-tag',
                                                             parent=header, alls=True)
                self.extract_salary(element[-1].text if element and element[-1] else '')
                # Job Type
                self.get_job_type(job_type=element[0].text if element and element[0] else '')
        except Exception as e:
            self.handle_exception(e)

    def extract_values_from_content(self, content: WebElement or None):
        try:
            element: WebElement or List[WebElement] or None
            if content:
                # Job Description with Tags
                self.job['job_description_tags']: str = content.get_attribute('innerHTML') if content else "N/A"
                # Job Description without Tags
                self.job['job_description']: str = content.text if content else "N/A"
        except Exception as e:
            self.handle_exception(e)

    def extract_values_from_company_section(self, company_section: WebElement or None):
        try:
            element: WebElement or List[WebElement] or None
            if company_section:
                # Company Name & Address
                element: WebElement = self.get_element(locator='h2', selector='tag', parent=company_section)
                self.job['company_name']: str = element.text if element else "N/A"
                # Company Address
                element: WebElement = self.get_element(selector='css', locator='h3:not(.listing-pill)',
                                                       parent=company_section)
                self.job['address']: str = element.text if element else "Remote"
        except Exception as e:
            self.handle_exception(e)

    def tab_visited(self, tab: str) -> bool:
        self.driver.switch_to.window(tab)
        try:
            header: WebElement = self.get_element(locator='/html/body/div[4]/div[2]/div[1]', selector='xpath')
            content: WebElement = self.get_element(locator='section.job div.listing-container', selector='css')
            company: WebElement = self.get_element(locator='/html/body/div[4]/div[2]/div[2]', selector='xpath')
            if header and company and content:
                time.sleep(1)
                self.extract_values_from_header(header=header)
                self.extract_values_from_content(content=content)
                self.extract_values_from_company_section(company_section=company)
                job = self.job.copy()
                self.scraped_jobs.append(job)
                self.driver.close()
                return True
            else:
                self.driver.close()
        except WebDriverException as e:
            self.handle_exception(e)
            self.driver.close()
            return False

    def find_jobs(self) -> None:
        try:
            urls: list[str] = self.extract_links()
            if len(urls) > 0:
                for url in urls:
                    try:
                        self.driver.execute_script(
                            "window.open('" + url + "', '_blank');")
                        visited: bool = self.tab_visited(self.driver.window_handles[-1])
                        if visited:
                            self.job.clear()
                            self.driver.switch_to.window(self.driver.window_handles[0])
                        else:
                            continue
                    except Exception as e:
                        self.handle_exception(e)
                        continue
            self.export_to_excel() if len(self.scraped_jobs) > 0 else None
            self.log_error_if_any() if len(self.errs) > 0 else None
            self.driver.quit()
        except Exception as e:
            self.handle_exception(e)
            self.log_error_if_any() if len(self.errs) > 0 else None
            self.driver.quit()

    def export_to_excel(self) -> None:
        columns_name: list[str] = ["job_title", "company_name", "job_posted_date", "address", "job_description",
                                   'job_source_url',
                                   "salary_format",
                                   "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                                   "job_description_tags"]
        df = pd.DataFrame(data=self.scraped_jobs, columns=columns_name)
        filename: str = generate_scraper_filename(ScraperNaming.WE_WORK_REMOTELY)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="We Work Remotely", filename=filename)

    def log_error_if_any(self) -> List[dict]:
        df = pd.DataFrame(self.errs)
        unique_df = df.drop_duplicates()
        errors = unique_df.to_dict(orient='records')
        unique_df.to_csv('scraper/job_data/weworkremotely_errors.csv', index=False)
        return errors


def weworkremotely(url: str, job_type: str = 'full time remote') -> None:
    WeWorkRemotelyScraper.call(url)
