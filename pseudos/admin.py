from django.contrib import admin
from pseudos.models import Skills, GenericSkills, Verticals
# Register your models here.

admin.site.register(GenericSkills)

admin.site.register(Skills)

admin.site.register(Verticals)
