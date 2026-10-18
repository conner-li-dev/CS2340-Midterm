from typing import override

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    
    @override
    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @override
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    reason = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @override
    def __str__(self) -> str:
        return str(self.id) + ' - ' + self.user.username

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    stars = models.PositiveSmallIntegerField(choices = [
        (value, f"{value} star {'s' if value != 1 else ''}") 
        for value in range(1,6)], 
        validators= [MinValueValidator(1), MaxValueValidator(5)],)
    
    class Meta:
        constraints = [
            models.CheckConstraint(check = models.Q(stars__gte = 1, stars__lte = 5),
                                   name = "rating_stars_between_1_and_5",
                                   ),
            models.UniqueConstraint(fields = ["movie", "user"],
                                    name = "Unique_user_movie_rating",),
        ]

    @override
    def __str__(self) -> str:
        return f"{self.movie.name} - {self.stars} stars by {self.user.username}"
