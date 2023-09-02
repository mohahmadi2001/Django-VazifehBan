from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager



class CustomUserManager(BaseUserManager):
    
    def get_by_natural_key(self, username):
        return self.get(username=username)
    
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted=False)

    def archives(self):
        return super().get_queryset().filter(is_deleted=True)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)  # Use normalize_email from BaseUserManager
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class SoftDeleteModel(models.Model):
    objects = CustomUserManager()

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