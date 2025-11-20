from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import models as octo_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        octo_models.User.objects.all().delete()
        octo_models.Team.objects.all().delete()
        octo_models.Activity.objects.all().delete()
        octo_models.Leaderboard.objects.all().delete()
        octo_models.Workout.objects.all().delete()

        # Create Teams
        marvel = octo_models.Team(name='Team Marvel')
        marvel.save()
        dc = octo_models.Team(name='Team DC')
        dc.save()

        # Create Users (EmbeddedField expects the full object, not just ID)
        ironman = octo_models.User(name='Iron Man', email='ironman@marvel.com', team=marvel)
        ironman.save()
        captain = octo_models.User(name='Captain America', email='cap@marvel.com', team=marvel)
        captain.save()
        batman = octo_models.User(name='Batman', email='batman@dc.com', team=dc)
        batman.save()
        superman = octo_models.User(name='Superman', email='superman@dc.com', team=dc)
        superman.save()

        # Create Activities (user as EmbeddedField)
        octo_models.Activity(user=ironman, type='Run', duration=30).save()
        octo_models.Activity(user=batman, type='Swim', duration=45).save()

        # Create Workouts
        octo_models.Workout(name='Morning Cardio', description='Cardio for all heroes').save()
        octo_models.Workout(name='Strength Training', description='Strength for all heroes').save()

        # Create Leaderboard (team as EmbeddedField)
        octo_models.Leaderboard(team=marvel, points=100).save()
        octo_models.Leaderboard(team=dc, points=90).save()

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
