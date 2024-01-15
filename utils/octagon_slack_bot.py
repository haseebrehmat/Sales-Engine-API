import datetime

from django.db.models import Sum
from slack import WebClient
from slack.errors import SlackApiError

from scraper.models import ScraperLogs
from settings.base import env

bot_message_template = """
:robot_face: *Scraping Status Report* :arrows_counterclockwise:

@here Hello team! :wave: Here's the latest update on our scraping activities:

:clock3: *Report Timestamp:* {current_time_stamp}

:large_green_circle: *Active Scrapers List:*
- {active_scrapers_list}

:large_yellow_circle: *Scrapers with Jobs Scraped, but Zero Uploads:*
- {warning_scrapers_list}

:red_circle: *Inactive Scrapers List:*
- {inactive_scrapers_list}

:bar_chart: *Statistical Insights:*
{scraper_status_report}
:chart_with_upwards_trend: *Overall Scraper Summary:*
- *Total Scraped Jobs :mag::* {total_scraped_jobs}
- *Total Uploaded Jobs :arrow_up::* {total_uploaded_jobs}

Remember, this report is generated every 2-3 hours to keep you in the loop. If you have any questions or concerns, feel free to reach out. Let's keep those scrapers running smoothly! :rocket:
"""

scraper_updated_template = """
- *{scraper}*:
-:mag: Total jobs scraped: {scraped}
-:arrow_up: Jobs uploaded: {uploaded}
"""


def send_message(msg=bot_message_template, channel='#scrapers-updates-bot'):
    # channel='#test'
    if env('ENVIRONMENT') == 'production' and env.bool('SLACK_BOT_NOTIFICATION_ENABLED'):
        client = WebClient(token=env('SLACK_API_TOKEN'))
        try:
            response = client.chat_postMessage(channel=channel, text=f"{msg}")
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")

def send_server_message(msg, channel='#scrapers-updates-bot'):
    # channel='#test'
    if env('ENVIRONMENT') == 'staging' and env.bool('SLACK_BOT_NOTIFICATION_ENABLED'):
        client = WebClient(token=env('SLACK_API_TOKEN'))
        try:
            response = client.chat_postMessage(channel=channel, text=f"{msg}")
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")

def notify_octagon_scraper_stats_via_slack():
    scrapers_count = {}
    production_scrapers = ['Builtin', 'Workable', 'WeWorkRemotely', 'Glassdoor', 'Zip Recruiter', 'Indeed', 'Linkedin',
                           'Simply Hired', 'RubyOnRemote', 'YCombinator', 'Remote ok', 'Just Remote', 'Monster', 'Dice', 'Talent']
    today = str(datetime.datetime.now())[:10]
    for job_source in production_scrapers:
        queryset = ScraperLogs.objects.filter(created_at__date=today, job_source=job_source)
        if queryset:
            result = queryset.aggregate(scraped_jobs=Sum('total_jobs'), uploaded_jobs=Sum('uploaded_jobs'))
            scrapers_count.update(
                {job_source: {'scraped': result['scraped_jobs'], 'uploaded': result['uploaded_jobs']}})
        else:
            scrapers_count.update({job_source: {'scraped': 0, 'uploaded': 0}})
    scraper_status_report = ''
    active_scrapers_list = []
    warning_scrapers_list = []
    inactive_scrapers_list = []
    total_scraped_jobs = 0
    total_uploaded_jobs = 0
    if scrapers_count:
        for scraper in scrapers_count:
            if scrapers_count[scraper]['scraped'] != 0:
                if scrapers_count[scraper]['uploaded'] != 0:
                    active_scrapers_list.append(scraper)
                else:
                    warning_scrapers_list.append(scraper)
            else:
                inactive_scrapers_list.append(scraper)
            total_scraped_jobs += scrapers_count[scraper]['scraped']
            total_uploaded_jobs += scrapers_count[scraper]['uploaded']
            scraper_status_report += f'{scraper_updated_template}'.format(scraper=scraper,
                                                                          scraped=scrapers_count[scraper]['scraped'],
                                                                          uploaded=scrapers_count[scraper]['uploaded'])
    current_time_stamp = datetime.datetime.now()
    octagon_scraper_report = f'{bot_message_template}'.format(current_time_stamp=current_time_stamp,
                                                              active_scrapers_list=format_list(active_scrapers_list),
                                                              warning_scrapers_list=format_list(warning_scrapers_list),
                                                              inactive_scrapers_list=format_list(
                                                                  inactive_scrapers_list),
                                                              scraper_status_report=scraper_status_report,
                                                              total_scraped_jobs=total_scraped_jobs,
                                                              total_uploaded_jobs=total_uploaded_jobs)
    print(octagon_scraper_report)
    if env('ENVIRONMENT') == 'production' and env.bool('SLACK_BOT_NOTIFICATION_ENABLED'):
        send_message(msg=octagon_scraper_report)


def format_list(scrapers_list):
    return ', '.join(scrapers_list) if scrapers_list else "None"
