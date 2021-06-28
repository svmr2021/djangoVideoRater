from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    url = models.URLField()
    category = models.CharField(max_length=30)
    author = models.CharField(max_length=30, default='')

    def rating_average(self, request):
        sum = 0
        ratings = Rating.objects.filter(video=self)
        for rating in ratings:
            sum += rating.stars
        if len(ratings)>0:
            return sum/len(ratings)
        else:
            return 0

    def __str__(self):
        return self.title


class Rating(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
    comments = models.TextField(max_length=100)

    class Meta:
        unique_together = (('user', 'video'),)
        index_together = (('user', 'video'),)
