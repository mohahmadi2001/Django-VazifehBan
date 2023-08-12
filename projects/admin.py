from django.contrib import admin
from .models import WorkSpace, Project, Sprint


@admin.register(WorkSpace)
class WorkSpaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    pass
