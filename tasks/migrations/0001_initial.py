
# Generated by Django 4.2.1 on 2023-08-11 17:17


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Label",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
            ],
            options={
                "verbose_name": "Label",
                "verbose_name_plural": "Labels",
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created Date"
                    ),
                ),
                ("start_date", models.DateTimeField(verbose_name="Start Date")),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "deadline",
                    models.DateTimeField(auto_now=True, verbose_name="Dead Line"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ToDo", "To Do"),
                            ("Doing", "Doing"),
                            ("Done", "Done"),
                        ],
                        max_length=255,
                        verbose_name="Status",
                    ),
                ),
                (
                    "sprint",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="projects.sprint",
                        verbose_name="Sprint ID",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tasks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task",
                "verbose_name_plural": "Tasks",
            },
        ),
        migrations.CreateModel(
            name="WorkTime",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateTimeField(auto_now_add=True)),
                ("end_date", models.DateTimeField(auto_now=True, null=True)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="work_times",
                        to="tasks.task",
                        verbose_name="Task",
                    ),
                ),
            ],
            options={
                "verbose_name": "Work Time",
                "verbose_name_plural": "Work times",
            },
        ),
        migrations.CreateModel(
            name="TaskLabel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "label",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="tasks.label",
                        verbose_name="Label",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="labels",
                        to="tasks.task",
                        verbose_name="Task",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task Label",
                "verbose_name_plural": "Task Labels",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(verbose_name="Content")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created Time"
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="tasks.task",
                        verbose_name="Task",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content",
                    models.FileField(
                        upload_to="task-attachments", verbose_name="Content"
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="tasks.task",
                        verbose_name="Task",
                    ),
                ),
            ],
            options={
                "verbose_name": "Attachment",
                "verbose_name_plural": "Attachments",
            },
        ),
    ]
