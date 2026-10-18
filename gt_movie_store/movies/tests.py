from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Movie, Rating


class RatingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="viewer")
        self.movie = Movie.objects.create(
            name="Example Movie",
            price=10,
            description="An example movie.",
            image="movie_images/example.jpg",
        )

    def test_stars_must_be_between_one_and_five(self):
        for stars in (0, 6):
            with self.subTest(stars=stars):
                rating = Rating(movie=self.movie, user=self.user, stars=stars)
                with self.assertRaises(ValidationError):
                    rating.full_clean()

    def test_a_user_can_rate_each_movie_once(self):
        Rating.objects.create(movie=self.movie, user=self.user, stars=5)
        duplicate = Rating(movie=self.movie, user=self.user, stars=4)

        with self.assertRaises(ValidationError):
            duplicate.full_clean()
