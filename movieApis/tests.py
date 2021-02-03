from django.test import TestCase,Client
from django.urls import reverse
from .models import Movie,Comment
import json
# from django.core import serializers
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
from django.db.models import Count
from datetime import datetime

class TestViews(TestCase):

    def setUp(self):
        self.client=Client()
        url = reverse('movies')
        my_data = {'title': 'jaws'}
        self.client.post(url, json.dumps(my_data), content_type='application/json')

        self.movies_list_url = reverse('movies')

        self.movies_details_url = reverse('movies')
        self.movies_details_url=self.movies_details_url+'?movie_id=1'
        #
        self.comments_list_url = reverse('comments')
        #
        self.movie_comments_list_url = reverse('comments')
        self.movie_comments_list_url = self.movie_comments_list_url+'?movie_id=1'
        #
        self.top_movies_url = reverse('top')
        self.top_movies_url = self.top_movies_url+'?start_date=2019-08-09&end_date=2019-08-10'


    def test_movies_POST(self):
        url = reverse('movies')
        my_data = {'title':'spiderman'}
        response = self.client.post(url,json.dumps(my_data), content_type='application/json')
        self.assertEquals(response.status_code,200)
        spiderman = Movie.objects.get(id=2)
        self.assertEquals(spiderman.title,'Spiderman')

    def test_movies_list_GET(self):
        response = self.client.get(self.movies_list_url)
        self.assertEquals(response.status_code,200)

    def test_movie_details_GET(self):
        response = self.client.get(self.movies_details_url)
        self.assertEquals(response.status_code, 200)

    def test_comments_POST(self):
        url = reverse('comments')
        my_data = {'comment': 'my first comment on Jaws','movie_id':1}
        response = self.client.post(url, json.dumps(my_data), content_type='application/json')
        self.assertEquals(response.status_code, 200)
        comment = Comment.objects.filter(movie_id=1)
        self.assertEquals(comment[0].comment,'my first comment on Jaws')

    def test_comments_list_GET(self):
        url = reverse('comments')
        my_data = {'comment': 'my first comment on Jaws', 'movie_id': 1}
        self.client.post(url, json.dumps(my_data), content_type='application/json')
        response = self.client.get(self.comments_list_url)
        self.assertEquals(response.status_code,200)
        comment = Comment.objects.all()
        print('len = ',len(comment))
        self.assertEquals(len(comment), 1)

    def test_movie_comments_list_GET(self):
        url = reverse('comments')
        my_data = {'comment': 'my first comment on Jaws', 'movie_id': 1}
        self.client.post(url, json.dumps(my_data), content_type='application/json')
        response = self.client.get(self.movie_comments_list_url)
        self.assertEquals(response.status_code,200)
        comment = Comment.objects.filter(movie_id=1)
        self.assertEquals(comment[0].comment, 'my first comment on Jaws')

    def test_top_movies_list_GET(self):
        #setup
        #added movie2
        url = reverse('movies')
        my_data = {'title': 'spiderman'}
        self.client.post(url, json.dumps(my_data), content_type='application/json')
        #added comment on movie1
        url = reverse('comments')
        my_data = {'comment': 'my first comment on Jaws', 'movie_id': 1}
        self.client.post(url, json.dumps(my_data), content_type='application/json')
        # added comment on movie2
        url = reverse('comments')
        my_data = {'comment': 'my first comment on spiderman', 'movie_id': 2}
        self.client.post(url, json.dumps(my_data), content_type='application/json')
        # added second comment on movie1
        url = reverse('comments')
        my_data = {'comment': 'my second comment on Jaws', 'movie_id': 1}
        self.client.post(url, json.dumps(my_data), content_type='application/json')
        #setup
        #assertion
        response = self.client.get(self.top_movies_url)
        self.assertEquals(response.status_code,200)
        today = datetime.now().date()
        dt_string = today.strftime("%Y-%m-%d")
        print(dt_string)
        comment = Comment.objects.filter(date__range=['2019-08-11', dt_string])
        comment = comment.values('movie_id').annotate(total_comments=Count('movie_id'))
        comment = comment.order_by('-total_comments')
        data = list(comment)
        a = {}
        rank = 1
        for item in data:
            num = item['total_comments']
            if num not in a:
                a[num] = rank
                item.update({'rank': rank})
                rank = rank + 1
            else:
                item.update({'rank': rank - 1})
        # print(data)
        self.assertEquals(data[0]['rank'], 1)
        self.assertEquals(data[1]['rank'], 2)