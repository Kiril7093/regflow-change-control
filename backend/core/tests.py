from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ChangeRequest


class SmokeTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="pass12345")

    def test_home_page_loads(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_change_request_list_requires_login(self):
        resp = self.client.get(reverse("change_request_list"))
        # should redirect to login
        self.assertEqual(resp.status_code, 302)

    def test_create_change_request_sets_created_by(self):
        self.client.login(username="u1", password="pass12345")
        resp = self.client.post(
            reverse("change_request_create"),
            data={
                "title": "Test CR",
                "change_type": "sop",
                "rationale": "Because reasons",
            },
        )
        self.assertEqual(resp.status_code, 302)
        cr = ChangeRequest.objects.get(title="Test CR")
        self.assertEqual(cr.created_by, self.user)
