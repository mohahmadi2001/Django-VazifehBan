# Generated by Django 4.2.1 on 2023-08-12 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="deadline",
        ),
        migrations.RemoveField(
            model_name="project",
            name="end_date",
        ),
        migrations.RemoveField(
            model_name="project",
            name="start_date",
        ),
        migrations.RemoveField(
            model_name="sprint",
            name="end_date",
        ),
        migrations.RemoveField(
            model_name="sprint",
            name="start_date",
        ),
        migrations.AddField(
            model_name="project",
            name="is_deleted",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name="sprint",
            name="is_deleted",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name="workspace",
            name="is_deleted",
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]