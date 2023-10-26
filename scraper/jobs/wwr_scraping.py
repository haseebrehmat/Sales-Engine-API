import math
import re
import time
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
        self.errs: List[str] = []

    def request_page(self) -> None:
        self.driver.get(self.url)

    @staticmethod
    def log_error(exception: Exception or str, save: bool = False) -> None:
        print(exception)
        saveLogs(exception) if save else None

    def home_page_loaded(self) -> bool:
        loaded: bool = False
        for retry in range(1, 6):
            try:
                self.request_page()
                homepage_element: WebElement = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'listing_column')
                    )
                )
                if not homepage_element:
                    time.sleep(3)
                main_element: list[WebElement] = self.driver.find_elements(
                    By.CLASS_NAME, 'listing_column')
                if main_element:
                    loaded = True
                    break
            except WebDriverException as e:
                if retry < 5:
                    print(f"Retry {retry}/{5} due to: {e}")
                else:
                    self.log_error(e, save=True)
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

    def get_element(self, locator: str, parent: WebElement = None, selector: str = 'class',
                    alls: bool = False) -> WebElement or List[WebElement] or None:
        try:
            by: str = By.CLASS_NAME
            if selector == 'css':
                by = By.CSS_SELECTOR
            if selector == 'xpath':
                by = By.XPATH
            if selector == 'tag':
                by = By.TAG_NAME
            if selector == 'name':
                by = By.NAME  # For Input fields
            wait: WebDriverWait = WebDriverWait(parent or self.driver, 10)
            ec: EC = EC.presence_of_all_elements_located((by, locator)) if alls else EC.presence_of_element_located(
                (by, locator))
            return wait.until(ec)
        except WebDriverException as e:
            self.errs.append(e.msg)
            return None

    def load_content(self) -> WebElement:
        return self.get_element(locator='section.job div.listing-container', selector='css')

    def load_company_details(self) -> WebElement:
        return self.get_element(locator='/html/body/div[4]/div[2]/div[2]', selector='xpath')

    def load_header(self) -> WebElement:
        return self.get_element(locator='/html/body/div[4]/div[2]/div[1]', selector='xpath')

    @staticmethod
    def extract_salary(salary: str) -> dict:
        pattern = r"\$(?P<min>[0-9,]+)(?:\s*-\s*\$(?P<max>[0-9,]+))?(\s+OR\s+MORE)?\s+(?P<format>[A-Z]+)"
        match = re.search(pattern, salary)
        if match:
            min_salary = match.group("min") or ""
            max_salary = match.group("max") or min_salary
            unit = match.group("format") or "USD"
            currency_format = "yearly" if int(max_salary.replace(',', '')) > 1000 else "monthly"
            return {
                "min": f"{min_salary}",
                "max": f"{max_salary}",
                "format": currency_format,
                "estimated": f"{min_salary} - {max_salary} {unit}"
            }
        else:
            return {
                "min": "N/A",
                "max": "N/A",
                "format": "N/A",
                "estimated": "N/A"
            }

    @staticmethod
    def get_job_type(job_type: str) -> str:
        if job_type == 'FULL-TIME':
            return 'full time remote'
        elif job_type == 'CONTRACT':
            return 'contract remote'
        else:
            'full time remote'

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

    def visit_tab(self, tab: str) -> None:
        element: WebElement or List[WebElement] or None
        self.driver.switch_to.window(tab)
        try:
            header: WebElement = self.load_header()
            content: WebElement = self.load_content()
            company: WebElement = self.load_company_details()
            if header and company and content:
                time.sleep(1)
                # Job Posted Date
                element: WebElement = self.get_element(locator='.listing-header-container time', selector='css',
                                                       parent=header)
                posted_date: str = self.parse_posted_date(element.get_attribute('datetime'))
                # Job Title
                element: WebElement = self.get_element(locator='.listing-header-container h1', selector='css',
                                                       parent=header)
                job_title: str = element.text if element else "N/A"
                # Job Description & Tags
                description_tags: str = content.get_attribute('innerHTML') if content else "N/A"
                description: str = content.text if content else "N/A"
                # Company Name & Address
                element: WebElement = self.get_element(locator='h2', selector='tag', parent=company)
                company_name: str = element.text if element else "N/A"
                element: WebElement = self.get_element(selector='css', locator='h3:not(.listing-pill)', parent=company)
                company_address: str = element.text if element else "Remote"
                # Salary Details & Job Type
                element: list[WebElement] = self.get_element(selector='css', locator='a span.listing-tag',
                                                             parent=header, alls=True)
                salary_details: dict = self.extract_salary(element[-1].text if element and element[-1] else '')
                job_type: str = self.get_job_type(job_type=element[0].text if element and element[0] else '')
                self.scraped_jobs.append({
                    "job_title": job_title,
                    "company_name": company_name,
                    "job_posted_date": posted_date,
                    "address": company_address,
                    "job_description": description,
                    "job_source_url": self.driver.current_url,
                    "salary_format": salary_details['format'],
                    "estimated_salary": salary_details['estimated'],
                    "salary_min": salary_details['min'],
                    "salary_max": salary_details['max'],
                    "job_source": "weworkremotely",
                    "job_type": job_type,
                    "job_description_tags": description_tags,
                })
                self.driver.close()
        except WebDriverException:
            self.driver.close()
            raise WebDriverException()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def find_jobs(self) -> None:
        try:
            urls: list[str] = self.extract_links()
            if len(urls) > 0:
                for url in urls:
                    try:
                        self.driver.execute_script(
                            "window.open('" + url + "', '_blank');")
                        self.visit_tab(self.driver.window_handles[-1])
                    except WebDriverException as e:
                        self.log_error(e, save=True)
                        continue
            if len(self.scraped_jobs) > 0:
                self.export_to_excel()
            self.driver.quit()
        except Exception as e:
            self.driver.quit()
            self.log_error(e, save=True)

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
            total_jobs=len(df), job_source="WeWorkRemotely", filename=filename)


def weworkremotely(url: str, job_type: str = 'full time remote') -> None:
    print("Running We Work Remotely...")
    try:
        driver: WebDriver = configure_webdriver(True)
        driver.maximize_window()
        wwr_scraper = WeWorkRemotelyScraper(
            driver=driver,
            url=url)
        wwr_scraper.find_jobs()
    except Exception as e:
        print(e)
        saveLogs(e)
    print("Done We Work Remotely...")
