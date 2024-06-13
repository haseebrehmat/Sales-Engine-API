import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scraper.constants.const import COLUMN_NAME, SALARY_FORMAT
from scraper.models import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, previous_jobs, set_job_type
from utils.helpers import log_scraper_running_time, saveLogs
from scraper.utils.helpers import configure_webdriver

from datetime import datetime, timedelta

total_job = 0

# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))

def extract_date(input_date, prefix = "Published on "):
    if input_date.startswith(prefix):
        input_date = input_date[len(prefix):]    
    return input_date

def is_one_week_ago(posted_date):
    try:
        current_date = datetime.now()
        one_week_ago_date = current_date - timedelta(days=7)
        converted_date = datetime.strptime(f"{posted_date} {current_date.year}", "%B %d %Y")
        return converted_date >= one_week_ago_date and converted_date <= current_date
    except ValueError:
        return False

def update_job_description(driver, data):
    current_url = driver.current_url
    try:
        for i in range(len(data)):
            driver.get(data[i][4])
            job_description = driver.find_elements(By.CLASS_NAME, "prose")[0]
            posted_date = driver.find_element(By.XPATH, "/html/body/main/section/div/div[1]/article/div[3]/h2")
            data[i][5] = extract_date(posted_date.text)
            data[i][3] = job_description.text
            data[i].append(job_description.get_attribute('innerHTML'))
    except Exception as e:
        saveLogs(e)
    driver.get(current_url)


# find's job name
def find_jobs(driver, job_type, total_job, link):
    try:
        request_url(driver, f'{link}')
        scrapped_data = []
        pagination_check = True

        job_section = driver.find_elements(By.TAG_NAME, "ul")[4]
        jobs = job_section.find_elements(By.TAG_NAME, "li")

        job_urls = [job.find_element(By.TAG_NAME, "a").get_attribute('href') for job in jobs if job.find_element(By.TAG_NAME, "a")]
        existing_jobs_dictionary = previous_jobs("ruby on remote", job_urls)
        count = 0

        original_window = driver.current_window_handle
        driver.switch_to.new_window('tab')
        for url in job_urls:
            try:
                if not existing_jobs_dictionary.get(url):
                    data = []
                    if count > 3:
                        pagination_check = False
                        break
                    driver.get(url)
                    tags = driver.find_element(By.TAG_NAME, "article")
                    tags.find_element(By.CLASS_NAME, "font-medium")
                    date = tags.find_element(By.CLASS_NAME, "font-medium").text
                    posted_date = date.split('Published on ')[1].split(',')[0]
                    fields = tags.text.split('\n')

                    if is_one_week_ago(posted_date):
                        if count > 0:
                            count-=1
                        data.append(fields[0])
                        company_name = driver.find_elements(By.TAG_NAME, "h3")[1].text
                        data.append(company_name)
                        if 'featured' in fields[1].lower():
                            data.append(fields[2])
                            job_type = fields[3]
                        else:
                            data.append(fields[1])
                            job_type = fields[2]

                        job_description = tags.find_element(By.CLASS_NAME, "trix-content")
                        data.append(job_description.text)
                        job_url = driver.current_url
                        data.append(job_url)
                        data.append(posted_date)
                        salary_format = "N/A"
                        estimated_salary = "N/A"
                        min_salary = "N/A"
                        max_salary = "N/A"
                        try:
                            format = tags.find_elements(By.TAG_NAME, "div")[1]
                            estimated_salary = format.find_elements(By.TAG_NAME, "span")[-1].text
                            if 'yearly' in estimated_salary.lower():
                                estimated_salary = estimated_salary.split(' Yearly')
                                salary_extrema = estimated_salary[0].split(" - ")
                                min_salary = salary_extrema[0]
                                salary_format = SALARY_FORMAT
                                max_salary = salary_extrema[1] if len(salary_extrema) > 1 else 'N/A'
                        except:
                            pass
                        data.append(salary_format)
                        data.append(estimated_salary[0])
                        data.append(min_salary)
                        data.append(max_salary)
                        data.append("Ruby On Remote")
                        data.append(set_job_type(job_type))
                        data.append(job_description.get_attribute("innerHTML"))
                        scrapped_data.append(data)
                    else:
                        if 'featured' not in fields[1].lower():
                            count+=1
            except:
                pass

        if len(scrapped_data) > 0:
            df = pd.DataFrame(data=scrapped_data, columns=COLUMN_NAME)
            filename = generate_scraper_filename(ScraperNaming.RUBY_ON_REMOTE)
            df.to_excel(filename, index=False)
            ScraperLogs.objects.create(total_jobs=len(df), job_source="RubyOnRemote", filename=filename)
        
        index = -1
        try:
            if pagination_check:
                driver.close()
                driver.switch_to.window(original_window)
                index = driver.find_elements(By.CLASS_NAME, "next")[0].get_attribute('class').find('disabled')
                return index == -1
            else:
                return False
        except Exception as e:
            saveLogs(e)
            return False

    except Exception as e:
        saveLogs(e)
        return False


# code starts from here
@log_scraper_running_time("Ruby on Remote")
def ruby_on_remote(link, job_type):
    base_link = link
    total_job = 0
    print("RubyOnRemote")
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        flag = True
        count = 0
        try:
            while flag:
                if count != 0:
                    link = f'{base_link}?page={count + 1}'
                flag = find_jobs(driver, job_type, total_job, link)
                count = count + 1
        except:
            pass

    except Exception as e:
        saveLogs(e)
    driver.quit()
