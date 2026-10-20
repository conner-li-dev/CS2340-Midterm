from typing import override

from django.contrib.auth.models import User
from django.db import models

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    review_count = models.IntegerField()
    purchase_count = models.IntegerField()
    
    
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
