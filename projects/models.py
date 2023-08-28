from datetime import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import SoftDeleteModel,TimeStampMixin
from tasks.models import Task
from accounts.models import Team
from django.utils import timezone



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
    
    def edit_workspace(self, new_title, new_team=None):
        self.title = new_title
        if new_team is not None:
            self.team = new_team
        self.save()
    
    
class Project(SoftDeleteModel,TimeStampMixin):
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    workspace = models.ForeignKey("WorkSpace",
                                  verbose_name=_("WorkSpace"),
                                  on_delete=models.CASCADE,
                                  related_name="projects")
    team = models.ForeignKey(Team, verbose_name=_("Team"), on_delete=models.CASCADE, related_name="projects", default=1)
    
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    
    
    def create_project(self, title, description, start_date, end_date, deadline):
        """Creates a new project.

        Args:
            title (str): Title of the project.
            description (str): Description of the project.
            start_date (datetime): Start date of the project.
            end_date (datetime): End date of the project.
            deadline (datetime): Deadline of the project.

        Returns:
            Project: The newly created project object.
        """
        project = Project.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            deadline=deadline,
            workspace=self.workspace
        )
        return project
    
    def get_project_info(self):
        return {
            "title": self.title,
            "description": self.description,
            "start_date": self.started_at.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": self.ended_at.strftime("%Y-%m-%d %H:%M:%S"),
            "deadline": self.deadline.strftime("%Y-%m-%d %H:%M:%S"),
        }
    
    def edit_project(self, **kwargs):
        Project.objects.filter(pk=self.pk).update(**kwargs)
    
    def __str__(self):
        return self.title
    
    
class Sprint(SoftDeleteModel, TimeStampMixin):
    project = models.ForeignKey("Project",
                                verbose_name=_("Project"),
                                on_delete=models.CASCADE,
                                related_name="sprints")
    
    started_at = models.DateTimeField(verbose_name=_("Started At"), default=timezone.now)


    class Meta:
        verbose_name = _("Sprint")
        verbose_name_plural = _("Sprints")

    def __str__(self):
        return f"Sprint {self.started_at.strftime('%Y-%m-%d')}"

    def create_sprint(self, start_date, end_date, project):
        """Creates a new sprint.

        Args:
            start_date (datetime): Start date of the sprint.
            end_date (datetime): End date of the sprint.
            project (Project): The associated project for the sprint.

        Returns:
            Sprint: The newly created sprint object.
        """
        sprint = Sprint.objects.create(
            started_at=start_date,
            ended_at=end_date, 
            project=project
        )
        return sprint

    def get_sprint_info(self):
        active_tasks = self.tasks.filter(end_date__gte=timezone.now())
        completed_tasks = self.tasks.filter(end_date__lt=timezone.now())
        return {
            "start_date": self.started_at,
            "end_date": self.ended_at,
            "project": self.project,
            "active_tasks": active_tasks,
            "completed_tasks": completed_tasks,
        }

    def edit_sprint(self, **kwargs):
        Sprint.objects.filter(pk=self.pk).update(**kwargs)