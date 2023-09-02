from django.test import TestCase

from accounts.models import CustomUser
from projects.models import Sprint
from .models import Task, Label, TaskLabel, WorkTime, Comment, Attachment


class TaskTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_task(self):
        title = 'Test Task'
        description = 'This is a test task'
        deadline = '2022-12-31 23:59:59'
        sprint = Sprint.objects.create(name='Test Sprint')
        user = CustomUser.objects.create_user(username='testuser', password='12345')
        status = 'ToDo'
        task = Task.create_task(title=title, description=description, deadline=deadline, sprint=sprint, user=user,
                                status=status)
        self.assertEqual(task.title, title)
        self.assertEqual(task.description, description)
        self.assertEqual(task.deadline.strftime('%Y-%m-%d %H:%M:%S'), deadline)
        self.assertEqual(task.sprint, sprint)
        self.assertEqual(task.user, user)
        self.assertEqual(task.status, status)

    def test_get_task(self):
        task = Task.create_task(title='Test Task', description='Test Description', deadline='2022-12-31 23:59:59',
                                sprint=None, user=None, status='ToDo')
        retrieved_task = Task.get_task(task.id)
        self.assertEqual(task, retrieved_task)

    def tast_update_task(self):
        task = Task.create_task(title='Test Task', description='Test Description', deadline='2022-12-31 23:59:59',
                                sprint=None, user=None, status='ToDo')
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.status, 'ToDo')
        Task.update_task(task.id, title='Updated Task', description='Updated Description', status='Done')
        task = Task.get_task(task.id)
        self.assertEqual(task.title, 'Updated Task')
        self.assertEqual(task.description, 'Updated Description')
        self.assertEqual(task.status, 'Done')

    def test_task_status(self):
        task1 = Task.create_task(title='Task 1', description='Description 1', deadline='2022-01-01', sprint=None,
                                 user=None, status='ToDo')
        task = Task.task_status('ToDo')
        self.assertEqual(task, task1)

    def tearDown(self) -> None:
        pass


class LabelTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_label(self):
        label_name = 'Valid Label'
        label = Label.create_label(label_name)
        self.assertIsInstance(label, Label)
        self.assertEqual(label.name, label_name)

    def test_get_label(self):
        label = Label.create_label(name='Test Label')
        result = Label.get_label(label.id)
        self.assertEqual(result, label)

    def test_all_tasks(self):
        label = Label.create_label(name='test_label')
        task1 = Task.create_task(title='test_task1', description='test_description1', deadline='2022-01-01 00:00:00',
                                 sprint=None, user=None, status='ToDo')
        task2 = Task.create_task(title='test_task2', description='test_description2', deadline='2022-01-01 00:00:00',
                                 sprint=None, user=None, status='Doing')
        TaskLabel.create_task_label(label_id=label.id, task_id=task1.id)
        TaskLabel.create_task_label(label_id=label.id, task_id=task2.id)
        tasks = label.all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertIn({'task': task1.id}, tasks)
        self.assertIn({'task': task2.id}, tasks)

    def tearDown(self) -> None:
        pass


class TaskLabelTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_task_label(self):
        label = Label.create_label(name='Test Label')
        task = Task.create_task(title='Test Task', description='Test Description', deadline='2022-12-31 23:59:59',
                                sprint=None, user=None, status='ToDo')
        task_label = TaskLabel.create_task_label(label_id=label.id, task_id=task.id)
        self.assertIsInstance(task_label, TaskLabel)
        self.assertEqual(task_label.label_id, label.id)
        self.assertEqual(task_label.task_id, task.id)

    def test_get_task_label(self):
        task_label = TaskLabel.create_task_label(1, 1)
        result = TaskLabel.get_task_label(task_label.id)
        self.assertEqual(result, task_label)

    def test_update_task_label(self):
        task_label = TaskLabel.create_task_label(1, 1)
        updated_task_label = task_label.update_task_label(task_label.id, label=2)
        self.assertEqual(updated_task_label.label_id, 2)
        self.assertEqual(updated_task_label.task_id, 1)

    def test_delete_task_label(self):
        task_label = TaskLabel.create_task_label(1, 1)
        task_label.delete_task_label()
        self.assertFalse(TaskLabel.does_task_label_exist(task_label))

    def tearDown(self) -> None:
        pass


class CommentTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_comment(self):
        task = Task.create_task(title='Test Task', description='Test Description', deadline='2022-12-31 23:59:59',
                                sprint=None, user=None, status='ToDo')
        comment = Comment.create_comment(content='Test Comment', user_id=1, task_id=task.id)
        self.assertEqual(comment.content, 'Test Comment')
        self.assertEqual(comment.user_id, 1)
        self.assertEqual(comment.task_id, task.id)

    def test_get_comment(self):
        comment = Comment.create_comment(content='test', user_id=1, task_id=1)
        result = Comment.get_comment(comment.id)
        self.assertEqual(result, comment)

    def test_update_comment(self):
        comment = Comment.create_comment(content='old content', user_id=1, task_id=1)
        Comment.update_comment(comment.id, content='new content')
        updated_comment = Comment.get_comment(comment.id)
        self.assertEqual(updated_comment.content, 'new content')

    def tearDown(self) -> None:
        pass


class AttachmentTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_attachment(self):
        task = Task.create_task(title='Test Task', description='Test Description', deadline='2022-12-31 23:59:59',
                                sprint=1, user=1, status='ToDo')
        attachment = Attachment.create_attachment(content='Test Content', task_id=task.id)
        self.assertEqual(attachment.content, 'Test Content')
        self.assertEqual(attachment.task_id, task.id)

    def test_get_attachment(self):
        attachment = Attachment.create_attachment(content='test', task_id=1)
        result = Attachment.get_attachment(attachment.id)
        self.assertEqual(result, attachment)

    def test_update_attachment(self):
        attachment = Attachment.create_attachment(content='test_content', task_id=1)
        Attachment.update_attachment(attachment.id, content='new_content', task_id=2)
        updated_attachment = Attachment.get_attachment(attachment.id)
        self.assertEqual(updated_attachment.content.name, 'task-attachments/new_content')
        self.assertEqual(updated_attachment.task_id, 2)

    def tearDown(self) -> None:
        pass


class WorkTimeTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_worktime(self):
        task = Task.create_task(title='Test Task', description='Test Description', deadline='2022-12-31 23:59:59',
                                sprint=1, user=1, status='ToDo')
        worktime = WorkTime.create_worktime(start_date='2022-12-31 23:59:59', task_id=task.id)
        self.assertIsInstance(worktime, WorkTime)
        self.assertEqual(worktime.start_date.strftime('%Y-%m-%d %H:%M:%S'), '2022-12-31 23:59:59')
        self.assertEqual(worktime.task.id, task.id)

    def test_get_worktime(self):
        worktime = WorkTime.create_worktime(start_date='2022-01-01', task_id=1)
        result = WorkTime.get_worktime(worktime.id)
        self.assertIsInstance(result, WorkTime)

    def test_update_worktime(self):
        worktime = WorkTime.create_worktime(start_date='2022-01-01 00:00:00', task_id=1)
        WorkTime.update_worktime(worktime.id, start_date='2022-01-02 00:00:00')
        updated_worktime = WorkTime.get_worktime(worktime.id)
        self.assertEqual(updated_worktime.start_date.strftime('%Y-%m-%d %H:%M:%S'), '2022-01-02 00:00:00')

    def test_complete_worktime(self):
        worktime = WorkTime.create_worktime(start_date='2022-01-01 00:00:00', task_id=1)
        end_date = '2022-01-02 00:00:00'
        worktime.complete_worktime(end_date)
        self.assertEqual(worktime.end_date.strftime('%Y-%m-%d %H:%M:%S'), end_date)

    def tearDown(self) -> None:
        pass
