from django.contrib import admin
from .models import Task, TaskLabel, WorkTime, Comment, Label, Attachment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskLabel)
class TaskLabelAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Label)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Attachment)
class LabelAdmin(admin.ModelAdmin):
    pass
