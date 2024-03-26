from flaskscrapper.models import ScrapersRunningStatus

ScrapersRunningStatus.objects.all().update(running=False, loop=False)