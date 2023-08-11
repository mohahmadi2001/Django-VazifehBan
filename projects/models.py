from datetime import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

from tasks.models import Task


class WorkSpace(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    team = models.ForeignKey("accounts.Team",
                             verbose_name=_("Team"),
                             on_delete=models.CASCADE,
                             related_name="workspaces"
                             )
    
    class Meta:
        verbose_name = _("WorkSpace")
        verbose_name_plural = _("WorkSpaces")
    
    def __str__(self):
        return self.title

    def create_project(self, title, description, start_date, end_date, deadline):
        project = Project.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            deadline=deadline,
            workspace=self,
        )
        return project

    def get_workspace_information(self):
        projects_list = [project.title for project in self.projects.all()]
        return {
            'title': self.title,
            'team': self.team.name,
            'projects': projects_list,
        }
    
    def edit_workspace(self, new_title):
        self.title = new_title
        self.save()
    
class Project(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    start_date = models.DateTimeField(_("Start Date"),auto_now_add=True)
    end_date = models.DateTimeField(_("End Date"))
    deadline = models.DateTimeField(_("Deadline"))
    workspace = models.ForeignKey("WorkSpace",
                                  verbose_name=_("WorkSpace"),
                                  on_delete=models.CASCADE,
                                  related_name="projects")
    
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    
    def create_sprint(self, start_date, end_date):
        sprint = Sprint.objects.create(
            start_date=start_date,
            end_date=end_date, 
            project=self
            )
        return sprint
    
    def get_active_sprints(self):
        return self.sprints.filter(end_date__gte=timezone.now())
    
    def get_completed_sprints(self):
        return self.sprints.filter(end_date__lt=timezone.now())
    
    def __str__(self):
        return self.title
    
    
class Sprint(models.Model):
    start_date = models.DateTimeField(_("Start Date"),auto_now_add=True)
    end_date = models.DateTimeField(_("End Date"))
    project = models.ForeignKey("Project",
                                verbose_name=_("Project"),
                                on_delete=models.CASCADE,
                                related_name="sprints")

    class Meta:
        verbose_name = _("Sprint")
        verbose_name_plural = _("Sprints")

    def __str__(self):
        return f"Sprint {self.start_date.strftime('%Y-%m-%d')}"
    
    def create_task(self, title, description, end_date, deadline, user=None, status=None):
        task = Task.objects.create(
            title=title,
            description=description,
            end_date=end_date,
            deadline=deadline,
            sprint=self,
            user=user,
            status=status
        )
        return task



