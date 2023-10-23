import re
import time

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
        self.scraped_jobs: list[dict] = []

    def request_page(self) -> None:
        self.driver.get(self.url)

    @staticmethod
    def log_error(exception: Exception or str, save: bool = False) -> None:
        print(exception)
        saveLogs(exception) if save else None

    def home_page_loaded(self) -> bool:
        loaded: bool = False
        for retry in range(5):
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
                if len(main_element) > 0:
                    loaded = True
                    break
            except WebDriverException as e:
                if retry + 1 < 5:
                    print(f"Retry {retry + 1}/{5} due to: {e}")
                else:
                    self.log_error(e, save=True)
                    self.driver.quit()
                    break
        return loaded

    def extract_links(self) -> list[str]:
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
                if len(anchor_elements) > 0 and anchor_elements[1]:
                    job_links.append(anchor_elements[1].get_attribute('href'))
        return job_links

    def load_content(self) -> WebElement:
        element: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'section.job div.listing-container')
            ))
        return element

    def load_company_details(self) -> WebElement:
        element: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[4]/div[2]/div[2]')
            ))
        return element

    def load_header(self) -> WebElement:
        element: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[4]/div[2]/div[1]')
            ))
        return element

    @staticmethod
    def extract_salary(salary: str) -> dict:
        pattern = r"\$(?P<min>[0-9,]+)(?:\s*-\s*\$(?P<max>[0-9,]+))?(\s+OR\s+MORE)?\s+(?P<format>[A-Z]+)"
        match = re.search(pattern, salary)
        if match:
            min_salary = match.group("min") or ""
            max_salary = match.group("max") or min_salary
            currency_format = match.group("format") or "USD"
            return {
                "min": f"${min_salary}",
                "max": f"${max_salary}",
                "format": currency_format,
                "estimated": f"${min_salary} - ${max_salary} ${currency_format}"
            }
        else:
            return {
                "min": "",
                "max": "",
                "format": "",
                "estimated": ""
            }

    @staticmethod
    def get_job_type(job_type: str) -> str:
        if job_type == 'FULL-TIME':
            return 'full time remote'
        elif job_type == 'CONTRACT':
            return 'contract remote'
        else:
            'full time remote'

    def visit_tab(self, tab: str) -> None:
        self.driver.switch_to.window(tab)
        try:
            header: WebElement = self.load_header()
            content: WebElement = self.load_content()
            company: WebElement = self.load_company_details()
            if header and company and content:
                time.sleep(1)
                # Posted Date
                posted_date_element: WebElement = WebDriverWait(header, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '.listing-header-container time')
                    ))
                posted_date: str = posted_date_element.get_attribute(
                    'datetime')
                # Job Title
                job_title_element: WebElement = WebDriverWait(header, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '.listing-header-container h1')
                    ))
                job_title: str = job_title_element.text
                # Job Description & Job Description Tags
                description_element: WebElement = self.load_content()
                description_tags: str = description_element.get_attribute(
                    'innerHTML')
                description: str = description_element.text
                # Company Name
                company_name_element: WebElement = WebDriverWait(company, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'h2'))
                )
                company_name: str = company_name_element.text
                # Company Address
                company_address_element: WebElement = WebDriverWait(company, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'h3:not(.listing-pill)'))
                )
                company_address: str = company_address_element.text
                # Salary
                badges_anchor_elements: list[WebElement] = WebDriverWait(header, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 'a span.listing-tag'))
                )
                salary_details: dict = self.extract_salary(
                    badges_anchor_elements[-1].text if badges_anchor_elements[-1] else '')
                # Job Type
                job_type_tag: str = badges_anchor_elements[0].text if badges_anchor_elements[0] else ''
                job_type: str = self.get_job_type(job_type=job_type_tag)
                self.scraped_jobs.append({
                    "job_title": job_title or "N/A",
                    "company_name": company_name or "N/A",
                    "job_posted_date": posted_date,
                    "address": company_address or "Remote",
                    "job_description": description or "N/A",
                    "job_source_url": self.driver.current_url,
                    "salary_format": salary_details.get("format", "N/A"),
                    "estimated_salary": salary_details.get("estimated", "N/A"),
                    "salary_min": salary_details.get("min", "N/A"),
                    "salary_max": salary_details.get("max", "N/A"),
                    "job_source": "weworkremotely",
                    "job_type": job_type,
                    "job_description_tags": description_tags or "N/A",
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


def weworkremotely() -> None:
    print("Running We Work Remotely...")
    try:
        driver: WebDriver = configure_webdriver()
        driver.maximize_window()
        wwr_scraper = WeWorkRemotelyScraper(
            driver=driver,
            url="https://weworkremotely.com/remote-jobs/search?search_uuid=&term=&sort=past_week&categories%5B%5D=2"
                "&categories%5B%5D=17&categories%5B%5D=18&categories%5B%5D=6&categories%5B%5D=11")
        wwr_scraper.find_jobs()
    except Exception as e:
        print(e)
        saveLogs(e)
    print("Done We Work Remotely...")
