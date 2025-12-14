from django.test import TestCase


class ActivitiesSmokeTest(TestCase):
    def test_imports(self):
        from .models import User, Team, Activity, Leaderboard, Workout
        self.assertIsNotNone(User)
        self.assertIsNotNone(Team)
        self.assertIsNotNone(Activity)
        self.assertIsNotNone(Leaderboard)
        self.assertIsNotNone(Workout)

    def test_api_endpoints(self):
        from django.urls import reverse
        endpoints = [
            'user-list', 'team-list', 'activity-list', 'leaderboard-list', 'workout-list'
        ]
        for endpoint in endpoints:
            url = reverse(endpoint)
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 403, 401])  # 403/401 if auth required
