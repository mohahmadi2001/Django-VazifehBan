from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from core.models import SoftDeleteModel, TimeStampMixin


class Task(SoftDeleteModel, TimeStampMixin):
    CHOICES = (
        ("ToDo", "To Do"),
        ("Doing", "Doing"),
        ("Done", "Done"),
    )
    title = models.CharField(_("Title"), max_length=255)
    created_at = models.DateTimeField(verbose_name=_("Created Date"),
                                      auto_now_add=True)
    description = models.TextField(_("Description"))
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

    @classmethod
    def create_task(cls: "Task", title, description, deadline, sprint, user, status):
        task = Task.objects.create(title=title,
                                   description=description,
                                   deadline=deadline,
                                   sprint=sprint,
                                   user=user,
                                   status=status)
        return task

    @classmethod
    def get_task(cls: "Task", id):
        task = get_object_or_404(Task, pk=id)
        return task

    def update_task(self: "Task", task_id, **kwargs):
        task = Task.get_task(task_id)
        for attr, value in kwargs.items():
            setattr(task, attr, value)
        task.save()

    def delete_task(self):
        self.delete()

    @property
    def all_labels(self: "Task"):
        labels = self.labels
        return labels

    @classmethod
    def task_status(cls: "Task", status):
        tasks = cls.objects.filter(status=status)
        return tasks

    @property
    def all_attachments(self: "Task"):
        attachments = self.attachments
        return attachments

    @property
    def all_comments(self: "Task"):
        comments = self.comments
        return comments

    @property
    def all_worktimes(self: "Task"):
        worktimes = self.work_times
        return worktimes


class Label(SoftDeleteModel):
    name = models.CharField(_("Name"),
                            max_length=255)

    @classmethod
    def create_label(self: "Label", name):
        label = Label.objects.create(name=name)
        return label

    @classmethod
    def get_label(self: "Label", id):
        label = get_object_or_404(Label, pk=id)
        return label

    def all_tasks(self):
        tasks = list(TaskLabel.objects.select_related("Task").filter(label=self.id).values("task"))
        return tasks

    def delete_label(self):
        self.delete()

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")

    def __str__(self):
        return self.name


class TaskLabel(SoftDeleteModel):
    label = models.ForeignKey("Label",
                              verbose_name=_("Label"),
                              null=True,
                              on_delete=models.SET_NULL)
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             null=True, on_delete=models.SET_NULL,
                             related_name="labels")

    @classmethod
    def create_task_label(cls: "TaskLabel", label_id, task_id):
        task_label = cls.objects.create(label=label_id, task=task_id)
        return task_label

    @classmethod
    def get_task_label(cls: "TaskLabel", id):
        task_label = get_object_or_404(TaskLabel, pk=id)
        return task_label

    def update_task_label(self: "TaskLabel", id, **kwargs):
        task_label = TaskLabel.get_task_label(id)
        for attr, value in kwargs.items():
            setattr(task_label, attr, value)
        task_label.save()

    def delete_task_label(self):
        self.delete()

    def does_task_label_exist(self):
        return TaskLabel.objects.filter(label=self.label, task=self.task).exists()

    class Meta:
        verbose_name = _("Task Label")
        verbose_name_plural = _("Task Labels")

    def __str__(self):
        return self.id


class Comment(SoftDeleteModel):
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

    @classmethod
    def create_comment(cls: "Comment", content, user_id, task_id):
        comment = cls.objects.create(content=content,
                                     user=user_id,
                                     task=task_id)
        return comment

    @classmethod
    def get_comment(cls: "Comment", id):
        comment = get_object_or_404(Comment, pk=id)
        return comment

    def update_comment(self: "Comment", id, **kwargs):
        comment = Comment.get_comment(id)
        for attr, value in kwargs.items():
            setattr(comment, attr, value)
        comment.save()

    def delete_comment(self):
        self.delete()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.content


class Attachment(SoftDeleteModel):
    content = models.FileField(_("Content"),
                               upload_to="task-attachments")
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             on_delete=models.CASCADE,
                             related_name="attachments")

    @classmethod
    def create_attachment(cls: "Attachment", content, task_id):
        attachment = cls.objects.create(content=content, task=task_id)
        return attachment

    @classmethod
    def get_attachment(cls: "Attachment", id):
        attachment = get_object_or_404(Attachment, pk=id)
        return attachment

    def update_attachment(self: "Attachment", id, **kwargs):
        attachment = Attachment.get_attachment(id)
        for attr, value in kwargs.items():
            setattr(attachment, attr, value)
        attachment.save()

    def delete_attachment(self):
        self.delete()

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        return f"Attachment {self.id}"


class WorkTime(SoftDeleteModel):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             on_delete=models.CASCADE,
                             related_name="work_times")

    @classmethod
    def create_worktime(cls: "WorkTime", start_date, task_id):
        worktime = cls.objects.create(start_date=start_date, task=task_id)
        return worktime

    @classmethod
    def get_worktime(cls: "WorkTime", id):
        worktime = get_object_or_404(WorkTime, pk=id)
        return worktime

    def update_worktime(self: "WorkTime", id, **kwargs):
        worktime = WorkTime.get_worktime(id)
        for attr, value in kwargs.items():
            setattr(worktime, attr, value)
        worktime.save()

    def complete_worktime(self: "WorkTime", enddate):
        self.end_date = enddate
        self.save()

    def delete_worktime(self):
        self.delete()

    class Meta:
        verbose_name = _("Work Time")
        verbose_name_plural = _("Work times")

    def __str__(self):
        return f"task: {self.task}, start time: {self.start_date.strftime('%Y - %m - %d')}"
