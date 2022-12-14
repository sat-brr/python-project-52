from django.test import TestCase, Client
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django.urls import reverse
from http import HTTPStatus
from task_manager.settings import load_test_data
from django.contrib.messages import get_messages
# Create your tests here.


class TestTask(TestCase):
    fixtures = ['task.json', 'user.json', 'status.json', 'label.json']

    def setUp(self):
        self.client = Client()
        self.user_1 = get_user_model().objects.first()
        self.user_2 = get_user_model().objects.last()
        self.client.force_login(self.user_1)
        self.status = Status.objects.first()
        self.label = Label.objects.first()
        self.task = Task.objects.first()
        self.test_data = load_test_data()
        self.count = Task.objects.count()

    def test_create_task(self):

        response = self.client.post(reverse('create_task'),
                                    data=self.test_data['new']['task'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('tasks_list'))

        task = Task.objects.get(name=self.test_data['new']['task']['name'])

        self.assertEqual(Task.objects.count(), self.count + 1)
        self.assertEqual(task.status.id,
                         self.test_data['new']['task']['status'])
        self.assertEqual(task.author.id,
                         self.test_data['new']['task']['author'])
        self.assertEqual(task.labels.first().pk,
                         self.test_data['new']['task']['labels'])

    def test_update_task(self):
        task = Task.objects.first()

        response = self.client.post(reverse('update_task', args=[task.id]),
                                    data=self.test_data['new']['task'])

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('tasks_list'))

        updated_task = Task.objects.get(pk=task.pk)

        self.assertEqual(updated_task.name,
                         self.test_data['new']['task']['name'])
        self.assertEqual(updated_task.executor.pk,
                         self.test_data['new']['task']['executor'])

    def test_delete_task(self):

        response = self.client.post(reverse('delete_task', args=[self.task.id]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual(Task.objects.count(), self.count - 1)

    def test_delete_another_author_task(self):
        self.client.force_login(self.user_2)

        response = self.client.post(reverse('delete_task', args=[self.task.id]))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        message = list(get_messages(response.wsgi_request))

        self.assertEqual(message[0].tags, 'error')
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTrue(Task.objects.filter(pk=self.task.id))
