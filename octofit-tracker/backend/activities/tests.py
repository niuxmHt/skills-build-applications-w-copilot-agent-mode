from django.test import TestCase


class ActivitiesSmokeTest(TestCase):
    def test_imports(self):
        # simple import test
        from .models import Activity
        self.assertIsNotNone(Activity)
