from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about=models.CharField(max_length=160)
    website = models.URLField(max_length=100)
    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    platform = models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name='watchlist')
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0.0)
    number_rating = models.IntegerField(default =0)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Review(models.Model):
    review_user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    description = models.TextField(max_length=200)
    watchlist = models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    update  = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.rating) + " | " + str(self.watchlist)
        
# # Create your models here.
# class Movie(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=200)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name