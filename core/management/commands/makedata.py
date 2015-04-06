from django.core.management.base import NoArgsCommand
from core.models import Game, User, Group, GameTag
from uuid import uuid4
from faker import Faker
import random
import warnings


class Command(NoArgsCommand):
    help = "Create a bunch of dummy data."

    @staticmethod
    def _generate_user(fake, prefix):
        """Generate a user object."""
        user_dict = {"email": prefix + '-' + fake.email(),
                     "first_name": fake.first_name(),
                     "last_name": fake.first_name(),
                     "date_joined": fake.date_time(),
                     "birthday": fake.date_time_this_year(),
                     "gender": random.choice(["M", "F", "O"])}
        return User(**user_dict)

    @staticmethod
    def _create_group(fake, users):
        """Generate and save a group object."""
        name = fake.company()
        g = Group(name=name)
        g.save()
        g.members = users
        g.save()
        return g

    @staticmethod
    def _generate_gametag(fake):
        """Generate a tag object."""
        return GameTag(value=fake.city())

    @staticmethod
    def _create_game(fake, prefix, group, tags):
        """Generate and save a tag object."""
        game_dict = {"name": ' '.join(fake.sentence().split(' ')[:2]).title(),
                     "description": fake.paragraph(),
                     "image": None,
                     "group": group,
                     "event_name": fake.word().capitalize()}
        g = Game(**game_dict)
        g.save()
        g.tags = tags
        g.date_published = fake.date_time()
        g.save()
        return g

    def handle_noargs(self, **options):
        with warnings.catch_warnings():
            # Fake gives us annoying runtime warnings, supress them
            warnings.simplefilter("ignore")
            fake = Faker()
            prefix = uuid4().hex[:8]

            # Make 100 users
            users = []
            for i in range(100):
                users.append(self._generate_user(fake, prefix))
            User.objects.bulk_create(users)
            self.stdout.write('Created 100 Users.')

            # Make 20 group
            all_users = User.objects.all()
            for i in range(20):
                users = random.sample(all_users, random.randint(1, 10))
                self._create_group(fake, users)
            self.stdout.write('Created 20 Groups.')

            # Make 30 tags
            tags = []
            for i in range(30):
                tags.append(self._generate_gametag(fake))
            GameTag.objects.bulk_create(tags)
            self.stdout.write('Created 30 GameTags.')

            # Make 100 games
            all_tags = GameTag.objects.all()
            groups = Group.objects.all()
            for i in range(100):
                group = random.choice(groups)
                tags = random.sample(all_tags, random.randint(0, 5))
                self._create_game(fake, prefix, group, tags)
            self.stdout.write('Created 100 Games.')
