from datetime import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import SoftDeleteModel,TimeStampMixin
from tasks.models import Task


class WorkSpace(SoftDeleteModel):
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
    
    def create_workspace(self, title, team):
        """Creates a new workspace.

        Args:
            title (str): Title of the workspace.
            team (Team): The associated team.

        Returns:
            WorkSpace: The newly created workspace object.
        """
        workspace = self.objects.create(
            title=title,
            team=team
        )
        return workspace


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
    
    def change_team(self, new_team):
        self.team = new_team
        self.save()
    
    
class Project(SoftDeleteModel,TimeStampMixin):
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    workspace = models.ForeignKey("WorkSpace",
                                  verbose_name=_("WorkSpace"),
                                  on_delete=models.CASCADE,
                                  related_name="projects")
    
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    
    
    def get_project_info(self):
        return {
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": self.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "deadline": self.deadline.strftime("%Y-%m-%d %H:%M:%S"),
        }
    
    def edit_project(self, **kwargs):
        Project.objects.filter(pk=self.pk).update(**kwargs)
    
    
    def get_active_sprints(self):
        return self.sprints.filter(end_date__gte=timezone.now())
    
    def get_completed_sprints(self):
        return self.sprints.filter(end_date__lt=timezone.now())
    
    def __str__(self):
        return self.title
    
    
class Sprint(SoftDeleteModel,TimeStampMixin):
    project = models.ForeignKey("Project",
                                verbose_name=_("Project"),
                                on_delete=models.CASCADE,
                                related_name="sprints")
    

    class Meta:
        verbose_name = _("Sprint")
        verbose_name_plural = _("Sprints")

    def __str__(self):
        return f"Sprint {self.start_date.strftime('%Y-%m-%d')}"
    

    def get_sprint_info(self):
        active_tasks = self.tasks.filter(end_date__gte=timezone.now())
        completed_tasks = self.tasks.filter(end_date__lt=timezone.now())
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "project": self.project,
            "active_tasks": active_tasks,
            "completed_tasks": completed_tasks,
        }

    def edit_sprint(self, **kwargs):
        Sprint.objects.filter(pk=self.pk).update(**kwargs)

