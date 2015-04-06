from django.core.management.base import NoArgsCommand
from core.models import Game, User, Group
from uuid import uuid4
from faker import Faker
import random
import warnings


class Command(NoArgsCommand):
    help = "Create a bunch of dummy data."

    @staticmethod
    def _create_user(fake, prefix):
        user_dict = {"email": prefix + '-' + fake.email(),
                     "first_name": fake.first_name(),
                     "last_name": fake.first_name(),
                     "date_joined": fake.date_time(),
                     "birthday": fake.date_time_this_year(),
                     "gender": random.choice(["M", "F", "O"])}
        return User(**user_dict)

    @staticmethod
    def _create_group(fake, users):
        name = fake.company()
        g = Group(name=name)
        g.save()
        g.members = users
        g.save()
        return g

    @staticmethod
    def _create_game(fake, prefix, group):
        game_dict = {"name": ' '.join(fake.sentence().split(' ')[:2]).title(),
                     "description": fake.paragraph(),
                     "image": None,
                     "date_published": fake.date_time_this_year(),
                     "group": group,
                     "event_name": fake.word().capitalize()}
        return Game(**game_dict)

    def handle_noargs(self, **options):
        with warnings.catch_warnings():
            # Fake gives us annoying runtime warnings, supress them
            warnings.simplefilter("ignore")
            fake = Faker()
            prefix = uuid4().hex[:8]

            # Make 100 users
            users = []
            for i in range(100):
                users.append(self._create_user(fake, prefix))
            User.objects.bulk_create(users)
            self.stdout.write('Created 100 Users.')

            # Make 20 group
            all_users = User.objects.all()
            for i in range(20):
                users = random.sample(all_users, random.randint(1, 10))
                self._create_group(fake, users)
            self.stdout.write('Created 20 Groups.')

            # Make 100 games
            games = []
            groups = Group.objects.all()
            for i in range(100):
                group = random.choice(groups)
                games.append(self._create_game(fake, prefix, group))
            Game.objects.bulk_create(games)

            self.stdout.write('Created 100 Games.')
