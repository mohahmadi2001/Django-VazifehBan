from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

# Create your models here.


class MyManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)

    def archives(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteModel(models.Model):
    objects = MyManager()

    is_deleted = models.BooleanField(default=False, db_index=True)

    def delete(self):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True
        
        
class TimeStampMixin:
    started_at = models.DateTimeField(_("Start time"))
    ended_at = models.DateTimeField(_("End time"))
    deadline = models.DateTimeField(_("Deadline"))