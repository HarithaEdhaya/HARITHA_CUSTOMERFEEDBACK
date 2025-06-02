from django.test import TestCase
from django.urls import reverse
from .models import Feedback

class FeedbackModelTest(TestCase):

    def setUp(self):
        self.feedback = Feedback.objects.create(
            name='Test User',
            email='test@example.com',
            message='This is a test feedback message.'
        )

    def test_feedback_creation(self):
        self.assertEqual(self.feedback.name, 'Test User')
        self.assertEqual(self.feedback.email, 'test@example.com')
        self.assertEqual(self.feedback.message, 'This is a test feedback message.')
        self.assertIsNotNone(self.feedback.created_at)

    def test_str_method(self):
        self.assertEqual(str(self.feedback), 'Test User - test@example.com')


class FeedbackViewTest(TestCase):

    def test_feedback_list_view_status_code(self):
        url = reverse('feedback_list')  # make sure your URL name is 'feedback_list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # Add more view tests as needed
