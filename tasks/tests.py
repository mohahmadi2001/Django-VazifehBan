from django.test import TestCase
from .models import Task, TaskLabel, WorkTime, Comment, Attachment

class TaskTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_task(self):
        pass

    def test_get_task(self):
        pass

    def tast_update_task(self):
        pass

    def test_task_status(self):
        pass

    def tearDown(self) -> None:
        pass


class LabelTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_label(self):
        pass

    def test_get_label(self):
        pass

    def test_all_tasks(self):
        pass

    def tearDown(self) -> None:
        pass


class TaskLabelTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_task_label(self):
        pass

    def test_get_task_label(self):
        pass

    def test_update_task_label(self):
        pass

    def test_delete_task_label(self):
        pass

    def tearDown(self) -> None:
        pass


class CommentTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_comment(self):
        pass

    def test_get_comment(self):
        pass

    def test_update_comment(self):
        pass

    def tearDown(self) -> None:
        pass


class AttachmentTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_attachment(self):
        pass

    def test_get_attachment(self):
        pass

    def test_update_attachment(self):
        pass

    def tearDown(self) -> None:
        pass


class WorkTimeTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_worktime(self):
        pass

    def test_get_worktime(self):
        pass

    def test_update_worktime(self):
        pass

    def test_complete_worktime(self):
        pass

    def tearDown(self) -> None:
        pass
    