from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class WorkSpace(models.Model):
    title = models.CharField(_("Title"), max_length=50)

    
    class Meta:
        verbose_name = _("WorkSpace")
        verbose_name_plural = _("WorkSpaces")

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    start_date = models.DateTimeField(_("Start Date"),auto_now_add=True)
    end_date = models.DateTimeField(_("End Date"))
    deadline = models.DateTimeField(_("Deadline"))
    workspace = models.ForeignKey(WorkSpace, verbose_name=_("WorkSpace"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    
    def __str__(self):
        return self.title
    
    
class Sprint(models.Model):
    start_date = models.DateTimeField(_("Start Date"),auto_now_add=True)
    end_date = models.DateTimeField(_("End Date"))
    project = models.ForeignKey(Project,
                                   verbose_name=_("Project"),
                                   on_delete=models.CASCADE
                                   )


    class Meta:
        verbose_name = _("Sprint")
        verbose_name_plural = _("Sprints")

    def __str__(self):
        return f"Sprint {self.start_date.strftime('%Y-%m-%d')}"



