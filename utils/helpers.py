from error_logger.models import Log
from django.utils import timezone
import traceback
from datetime import datetime
import os
import requests
import rollbar
from django.forms.models import model_to_dict
from settings.base import env
from selenium.webdriver.common.by import By

from django.conf import settings

def validate_request(request, permissions):
    try:
        user_permissions = request.user.roles.permissions.values_list("codename", flat=True)
    except Exception as e:
        return False
    if request.method in permissions.keys():
        if permissions[request.method] is not None:
            for perm in permissions[request.method]:
                if perm in user_permissions:
                    return True
    return False


def saveLogs(exception, level='ERROR', request=None):
    try:
        path = None
        line_number = None
        error_message = None
        error_line = None
        method = None
        status_code = None
        user_id = None
        traceback_log = traceback.format_exc()
        if request:
            if hasattr(request, 'user') and request.user.is_authenticated:
                user_id = request.user
        traceback_data = []
        if hasattr(exception, '__traceback__'):
            traceback_data = traceback.extract_tb(exception.__traceback__)
        if len(traceback_data) > 0:
            path = traceback_data[0].filename
            error_line = traceback_data[0].line
            line_number = traceback_data[0].lineno
        log = Log(
            user_id=user_id,
            level=level,
            log_message=str(exception),
            error_message=error_message,
            error_line=error_line,
            traceback=traceback_log,
            path=path,
            line_number=line_number,
            method=method,
            status_code=status_code,
            time=timezone.now()
        )
        log.save()
        # Save error on rollbar if enabled
        if env.bool('ROLLBAR_ENABLED', False):
            data = model_to_dict(log)   
            rollbar.report_exc_info(extra_data=data)
    except Exception as e:
        print(e)

def send_request_to_flask(payload):
    try:
        base_url = os.getenv("FLASK_API_URL")
        url = f"{base_url}/run-scraper"
        headers = {
            "content-type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        return response.status_code == 200

    except Exception as e:
        print(str(e))
        return False


def log_scraper_running_time(job_source):
    def time_decorator(func):
        def wrapper(*args, **kwargs):
            url, _ = args
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            elapsed_seconds = (end_time - start_time).total_seconds()
            elapsed_minutes = elapsed_seconds / 60
            elapsed_hours = elapsed_minutes / 60
            if elapsed_seconds < 60:
                elapsed_time_str = f"{elapsed_seconds:.2f} seconds"
            elif elapsed_minutes < 60:
                elapsed_time_str = f"{elapsed_minutes:.2f} minutes"
            else:
                elapsed_time_str = f"{elapsed_hours:.2f} hours"
            msg = (
                f"[ Job Source: {job_source} ]--------"
                f"[ Started At: {start_time.strftime('%b %d, %Y %I:%M:%S %p')} ]--------"
                f"[ Ended At: {end_time.strftime('%b %d, %Y %I:%M:%S %p')} ]--------"
                f"[ Time Taken: {elapsed_time_str} ]--------"
                f"[ Link: {url} ]"
            )
            saveLogs(msg, 'INFO')
            return result
        return wrapper
    return time_decorator


def is_cloudflare(driver, source=''):
    try:
        cloudflare_footer = driver.find_element(By.ID, "footer-text")
        cloudflare_text = cloudflare_footer.text.lower() if cloudflare_footer else ""
        flag = "cloudflare" in cloudflare_text
        if flag:
            saveLogs(f"{source} Scraper got blocked due to Cloudflare Captcha.")
        return flag
    except:
        return False
    
def take_screenshot(driver, filename='ss'):
    screenshot_folder = os.path.join(settings.BASE_DIR, 'screenshots')
    os.makedirs(screenshot_folder, exist_ok=True)
    driver.save_screenshot(os.path.join(screenshot_folder, f"{filename}.png"))
