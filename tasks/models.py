from django.db import models
from django.utils.translation import gettext as _


class Task(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    start_date = models.DateTimeField(_("Start Date"), auto_now=True, null=True)
    end_date = models.DateTimeField(_("End Date"), auto_now=True, null=True)
    deadline = models.DateTimeField(_("Dead Line"), auto_now=True)
    sprint = models.ForeignKey("projects.Sprint", verbose_name=_("Sprint ID"), on_delete=models.CASCADE, related_name="tasks")
    user = models.ForeignKey("accounts.User", verbose_name=_("User"), null=True, on_delete=models.SET_NULL, related_name="tasks")
    status = models.ForeignKey("Status", verbose_name=_("Status"), null=True, on_delete=models.SET_NULL)


class Label(models.Model):
    name = models.CharField(_("Name"), max_length=255)


class Status(models.Model):
    name = models.CharField(_("Name"))


class TaskLabel(models.Model):
    label = models.ForeignKey("Label", verbose_name=_("Label"),null=True, on_delete=models.SET_NULL)
    task = models.ForeignKey("Task", verbose_name=_("Task"), null=True, on_delete=models.SET, related_name="labels")


class Comment(models.Model):
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created Time"), auto_now_add=True)
    user = models.ForeignKey("accounts.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey("Task", verbose_name=_("Task"), on_delete=models.CASCADE, related_name="comments")


class Attachment(models.Model):
    content = models.FileField(_("Content"), upload_to="task-attachments")
    task = models.ForeignKey("Task", verbose_name=_("Task"), on_delete=models.CASCADE, related_name="attachments")
