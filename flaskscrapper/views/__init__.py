from flaskscrapper.models import ScraperRunningStatus, ScrapersLoopStatus

ScraperRunningStatus.objects.filter(status=True).update(status=False)
ScrapersLoopStatus.objects.filter(loop_status=True).update(loop_status=False)