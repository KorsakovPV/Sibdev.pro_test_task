from django.contrib import admin

from priorities.models import PrioritiesNameModel, PrioritiesModel


@admin.register(PrioritiesNameModel)
class PrioritiesNameModelAdmin(admin.ModelAdmin):
    pass


@admin.register(PrioritiesModel)
class PrioritiesModelAdmin(admin.ModelAdmin):
    pass
