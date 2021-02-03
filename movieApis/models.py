from django.db import models
import datetime
# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100,blank=True)
    year = models.IntegerField(null=True,blank=False)
    rated = models.CharField(max_length=10,null=True,blank=False)
    released = models.DateField(null=True,blank=False)
    runtime = models.CharField(max_length=15,null=True,blank=False)
    genre=models.CharField(max_length=200,null=True,blank=False)
    director=models.CharField(max_length=50,null=True,blank=False)
    writer=models.CharField(max_length=500,null=True,blank=False)
    actors=models.CharField(max_length=500,null=True,blank=False)
    plot=models.CharField(max_length=1000,null=True,blank=False)
    language=models.CharField(max_length=20,null=True,blank=False)
    country=models.CharField(max_length=20,null=True,blank=False)
    awards=models.CharField(max_length=200,null=True,blank=False)
    poster=models.CharField(max_length=1000,null=True,blank=False)
    metascore=models.IntegerField(null=True,blank=False)
    imdbRating=models.FloatField(null=True,blank=False)
    imdbVotes=models.CharField(max_length=20,null=True,blank=False)
    imdbID=models.CharField(max_length=100,null=True,blank=False)
    Type=models.CharField(max_length=10,null=True,blank=False)
    DVD=models.DateField(null=True,blank=False)
    boxOffice=models.CharField(max_length=20,null=True,blank=False)
    production=models.CharField(max_length=100,null=True,blank=False)
    website=models.CharField(max_length=100,null=True,blank=False)

    def __int__(self):
        return self.id


class Comment(models.Model):

    comment = models.CharField(max_length=2000,blank=True)

    movie_id = models.ForeignKey(Movie,on_delete=models.CASCADE)

    date = models.DateField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.comment

    def __int__(self):
        return self.movie_id
