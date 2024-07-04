
from logging import exception
from datetime import timedelta, datetime
import pandas as pd
from selenium.webdriver.common.by import By
from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type, sleeper, previous_jobs
from utils.helpers import saveLogs, log_scraper_running_time
from scraper.jobs.base_scraper import BaseScraper


class JustRemoteScraper(BaseScraper):
    def __init__(self, url: str):
        super().__init__(url=url)

    def load_jobs(self):
        self.driver.get(self.url)
        previous_jobs = self.get_element(locator='hxecsD', alls=True)
        previous_len = len(previous_jobs)
        while True:
            if not self.check_if_job_day_ago(previous_jobs[previous_len-1]):
                break
            sleeper()
            self.driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
            previous_jobs = self.get_element(locator='hxecsD', alls=True)
            if previous_len == len(previous_jobs):
                break
            previous_len = len(previous_jobs)

        return previous_jobs

    def check_if_job_day_ago(self, job):
        day_ago = False
        try:
            date_elm = self.get_element(
                locator='new-job-item__JobItemDate-sc-1qa4r36-5', parent=job).text
            date_obj = datetime.strptime(date_elm, "%d %b")
            current_year = datetime.now().year
            date_obj = date_obj.replace(year=current_year)
            current_date = datetime.now()
            one_day_ago_date = current_date - timedelta(days=1)
            if date_obj >= one_day_ago_date:
                day_ago = True
        except Exception as e:
            saveLogs(e)
        return day_ago

    def get_job_urls(self):
        job_elements = self.load_jobs()
        links = []
        for job_element in job_elements:
            if not self.check_if_job_day_ago(job_element):
                continue
            link = self.get_element(
                selector='tag', locator='a', parent=job_element)
            t = self.get_element(
                locator="new-job-item__JobItemDate-sc-1qa4r36-5", parent=job_element)
            links.append([link.get_attribute("href"), t.text])
        return links

    def find_jobs(self):
        links = self.get_job_urls()
        curr_links = []
        for link in links:
            curr_links.append(link[0])
        self.get_previous_jobs(
            job_source=ScraperNaming.JUST_REMOTE, urls=curr_links)
        original_window = self.driver.current_window_handle
        for link in links:
            data = []
            if self.previous_links.get(link[0]):
                continue
            try:
                self.driver.switch_to.new_window('tab')
                self.driver.get(link[0])
                sleeper()
                job_type_check = self.get_element(
                    locator='job-meta__Wrapper-oh0pn7-0', alls=True)[0].text.lower()
                if 'contract' in job_type_check:
                    self.job['job_type'] = set_job_type('contract')
                elif 'permanent' in job_type_check:
                    self.job['job_type'] = set_job_type('full time')
                else:
                    continue
                temp = self.get_element(
                    locator='JpOdR')
                job_title = self.get_element(
                    locator='job-title__StyledJobTitle-sc-10irtcq-0', parent=temp)
                self.job['job_title'] = job_title.text
                company_name = self.get_element(
                    locator='ktyJgG')
                self.job['company_name'] = company_name.text.splitlines()[0]
                self.job['address'] = 'Remote'
                self.job['job_source_url'] = link[0]
                self.job['job_description'] = temp.text
                self.job['job_posted_date'] = link[1]
                self.job['salary_format'] = 'N/A'
                self.job['estimated_salary'] = 'N/A'
                self.job['salary_min'] = 'N/A'
                self.job['salary_max'] = 'N/A'
                self.job['job_source'] = ScraperNaming.JUST_REMOTE
                self.job['job_description_tags'] = temp.get_attribute(
                    'innerHTML')
            except exception as e:
                saveLogs(e)
            self.driver.close()
            self.driver.switch_to.window(original_window)
            self.scraped_jobs.append(self.job)
            self.job = {}
        if len(self.scraped_jobs) > 0:
            self.export_to_excel(ScraperNaming.JUST_REMOTE, 'Just Remote')


# code starts from here
@log_scraper_running_time('JustRemote')
def just_remote(link, job_type):
    try:
        justremote_scraper = JustRemoteScraper(url=link)
        justremote_scraper.find_jobs()
    except Exception as e:
        saveLogs(e)
    finally:
        justremote_scraper.delete_self()
