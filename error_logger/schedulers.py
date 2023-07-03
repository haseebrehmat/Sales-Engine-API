import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from error_logger.models import Log
from utils.helpers import saveLogs


# this function will delete Logs older than 15 days.
def delete_logs():
    try:
        print('Deleting logs ...')
        last_date = datetime.datetime.today() - datetime.timedelta(15)
        logs = Log.objects.filter(time__lte=str(last_date.date()))
        logs.delete()
    except Exception as e:
        saveLogs(e)


def run_delete_logs_scheduler():
    print('Create Delete Logs Scheduler ...')
    delete_logs_scheduler = BackgroundScheduler()
    # delete logs scheduler job will run at 6 am.
    delete_logs_scheduler.add_job(delete_logs, "cron", hour=6, minute=0)
    delete_logs_scheduler.start()