from django.db import models
from django.utils.translation import gettext as _


class Task(models.Model):
    CHOICES = (
        ("ToDo", "To DO"),
        ("Doing", "Doing"),
        ("Done", "Done"),
    )
    title = models.CharField(_("Title"), max_length=255)
    created_at = models.DateTimeField(verbose_name=_("Created Date"),
                                      auto_now_add=True)
    description = models.TextField(_("Description"))
    deadline = models.DateTimeField(_("Dead Line"), auto_now=True)
    sprint = models.ForeignKey("projects.Sprint",
                               verbose_name=_("Sprint ID"),
                               on_delete=models.CASCADE,
                               related_name="tasks")
    user = models.ForeignKey("accounts.CustomUser",
                             verbose_name=_("User"),
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name="tasks")
    status = models.CharField(_("Status"), choices=CHOICES, max_length=255)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.title


class Label(models.Model):
    name = models.CharField(_("Name"),
                            max_length=255)

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    label = models.ForeignKey("Label",
                              verbose_name=_("Label"),
                              null=True,
                              on_delete=models.SET_NULL)
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             null=True, on_delete=models.SET_NULL,
                             related_name="labels")

    class Meta:
        verbose_name = _("Task Label")
        verbose_name_plural = _("Task Labels")

    def __str__(self):
        return self.id


class Comment(models.Model):
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created Time"),
                                      auto_now_add=True)
    user = models.ForeignKey("accounts.CustomUser",
                             verbose_name=_("User"),
                             on_delete=models.CASCADE,
                             related_name="comments")
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             on_delete=models.CASCADE,
                             related_name="comments")

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.content


class Attachment(models.Model):
    content = models.FileField(_("Content"),
                               upload_to="task-attachments")
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             on_delete=models.CASCADE,
                             related_name="attachments")

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        return self.id


class WorkTime(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True,
                                    null=True)
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             on_delete=models.CASCADE,
                             related_name="work_times")

    class Meta:
        verbose_name = _("Work Time")
        verbose_name_plural = _("Work times")

    def __str__(self):
        return self.id
