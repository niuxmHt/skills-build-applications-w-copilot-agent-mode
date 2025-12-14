from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from activities.models import Activity
from djongo import models as djongo_models
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Teams
        marvel_team = {'name': 'Team Marvel', 'description': 'Marvel superheroes'}
        dc_team = {'name': 'Team DC', 'description': 'DC superheroes'}
        marvel_team_id = db.teams.insert_one(marvel_team).inserted_id
        dc_team_id = db.teams.insert_one(dc_team).inserted_id

        # Users
        users = [
            {'name': 'Tony Stark', 'email': 'tony@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Steve Rogers', 'email': 'steve@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Bruce Wayne', 'email': 'bruce@dc.com', 'team_id': dc_team_id},
            {'name': 'Clark Kent', 'email': 'clark@dc.com', 'team_id': dc_team_id},
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user_email': 'tony@marvel.com', 'type': 'run', 'distance': 5, 'duration': 30},
            {'user_email': 'steve@marvel.com', 'type': 'cycle', 'distance': 20, 'duration': 60},
            {'user_email': 'bruce@dc.com', 'type': 'swim', 'distance': 2, 'duration': 40},
            {'user_email': 'clark@dc.com', 'type': 'fly', 'distance': 100, 'duration': 10},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user_email': 'tony@marvel.com', 'points': 100},
            {'user_email': 'steve@marvel.com', 'points': 90},
            {'user_email': 'bruce@dc.com', 'points': 95},
            {'user_email': 'clark@dc.com', 'points': 110},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user_email': 'tony@marvel.com', 'workout': 'Ironman training'},
            {'user_email': 'steve@marvel.com', 'workout': 'Shield throws'},
            {'user_email': 'bruce@dc.com', 'workout': 'Batcave HIIT'},
            {'user_email': 'clark@dc.com', 'workout': 'Kryptonian sprints'},
        ]
        db.workouts.insert_many(workouts)

        # Ensure unique index on email
        db.users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
