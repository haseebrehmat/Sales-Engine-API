from django.contrib import admin
from pseudos.models import Skills, GenericSkills
# Register your models here.

admin.site.register(GenericSkills)

admin.site.register(Skills)
from pseudos.models import SectionStatus
# Register your models here.
admin.site.register(SectionStatus)
# admin.site.register(Verticals)
