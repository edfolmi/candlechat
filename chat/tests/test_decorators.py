from django.test import RequestFactory, TestCase
from django.http import HttpResponse
from django.contrib.auth.models import User

from chat.decorators import only_authenticated


def test_view(request):
    return HttpResponse("user must login!")


@only_authenticated
def authenticated_test_view(request):
    return HttpResponse("Authenticated")


class DecoratorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', password='test12345')

    def test_non_authenticated_user(self):
        request = self.factory.get('/')
        response = test_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"user must login!")

    def test_authenticated_user(self):
        request = self.factory.get('/')
        request.user = self.user  # Assign the user to request.user
        response = authenticated_test_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Authenticated")
