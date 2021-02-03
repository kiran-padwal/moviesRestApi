from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import requests
import json
import datetime
from movieApis.models import Movie,Comment
from django.core import serializers
from django.db.models import Count



@csrf_exempt
def movies(request):
    if request.method == 'GET':
        try:
            movie_id = request.GET.get('movie_id', '')
            released_year = request.GET.get('released_year', '')
            genre = request.GET.get('genre', '')
            if movie_id:
                movie = Movie.objects.filter(id=movie_id)
            elif released_year:
                movie = Movie.objects.filter(year=released_year)
            elif movie_id and released_year:
                movie = Movie.objects.filter(year=released_year).filter(id=movie_id)
            elif genre:
                movie = Movie.objects.filter(genre__icontains=genre)
            else:
                movie = Movie.objects.all()
            response = serializers.serialize('json', movie)
        except Exception as e:
            print(e)
            response = json.dumps([{'Error': 'exception occured'}])
        return HttpResponse(response, content_type='application/json')
    if request.method == 'POST':
        payload = json.loads(request.body)
        title = payload['title']
        print(title)
        if title:
            try:
                omdb_response = requests.get(url='http://www.omdbapi.com/?t='+title+'&apikey=81dd8d72&type=movie')
                omdb_response_json = omdb_response.json()
                # print(omdb_response_json)
                # print(omdb_response_json['Title'])

                year = omdb_response_json['Year']
                if year == 'N/A':
                   year = None
                else:
                    year = int(omdb_response_json['Year'])

                metascore = omdb_response_json['Metascore']
                if metascore == 'N/A':
                    metascore = None
                else:
                    metascore = int(omdb_response_json['Metascore'])

                released = omdb_response_json['Released']
                if released == 'N/A':
                    released = None
                else:
                    released = datetime.datetime.strptime(released, "%d %b %Y")
                    released = datetime.date.strftime(released.date(), '%Y-%m-%d')

                DVD = omdb_response_json['DVD']
                if DVD == 'N/A':
                    DVD = None
                else:
                    DVD = datetime.datetime.strptime(DVD, "%d %b %Y")
                    DVD = datetime.date.strftime(DVD.date(), '%Y-%m-%d')

                try:
                    # check if movie exits
                    entry = Movie.objects.get(imdbID=omdb_response_json['imdbID'])
                    print("Entry contained in queryset")
                    response = json.dumps([{'Error': 'Movie already present!'}])
                    return HttpResponse(response, content_type='application/json')
                except Exception as e:
                    print(e)
                    pass
                    try:
                        movie = Movie(
                            title=omdb_response_json['Title'], year=year, rated=omdb_response_json['Rated'],
                            released=released, runtime=omdb_response_json['Runtime'], genre=omdb_response_json['Genre'],
                            director=omdb_response_json['Director'], writer=omdb_response_json['Writer'],
                            actors=omdb_response_json['Actors'],
                            plot=omdb_response_json['Plot'], language=omdb_response_json['Language'],
                            country=omdb_response_json['Country'],
                            awards=omdb_response_json['Awards'], poster=omdb_response_json['Poster'],
                            metascore=metascore,
                            imdbRating=float(omdb_response_json['imdbRating']),
                            imdbVotes=omdb_response_json['imdbVotes'], imdbID=omdb_response_json['imdbID'],
                            Type=omdb_response_json['Type'], DVD=DVD, boxOffice=omdb_response_json['BoxOffice'],
                            production=omdb_response_json['Production'], website=omdb_response_json['Website']
                        )
                        movie.save()
                        latest_obj = Movie.objects.latest('id')
                        movie_data = Movie.objects.get(id=latest_obj.id)
                        data = serializers.serialize('json', [movie_data, ])
                        struct = json.loads(data)
                        data = json.dumps(struct[0])
                        return HttpResponse(data, content_type='application/json')
                    except:
                        response = json.dumps([{'Error': 'Movie could not be added!'}])
                        return HttpResponse(response, content_type='application/json')
            except Exception as e:
                print(e)
                response = json.dumps([{'Error': 'omdbiapi failed to sent response '}])
                return HttpResponse(response, content_type='application/json')
        else:
            response = json.dumps([{ 'Error': 'tittle cannot be empty'} ])
            return HttpResponse(response, content_type='application/json')



@csrf_exempt
def comments(request):
    if request.method == 'GET':
        try:
            movie_id=request.GET.get('movie_id', '')
            if movie_id:
                comment = Comment.objects.filter(movie_id=movie_id)
            else:
                comment = Comment.objects.all()
            response = serializers.serialize('json', comment)
        except Exception as e:
            print(e)
            response = json.dumps([{'Error': 'exception occured '}])
        return HttpResponse(response, content_type='application/json')
    if request.method == 'POST':
        payload = json.loads(request.body)
        comment_text = payload['comment']
        movie_id = payload['movie_id']
        # print(comment_text)
        try:
            movie_obj = Movie.objects.get(id=movie_id)
            print(movie_obj)
            comment = Comment(comment=comment_text, movie_id=movie_obj)
            comment.save()
            latest_obj = Comment.objects.latest('id')
            comment_data = Comment.objects.get(id=latest_obj.id)
            data = serializers.serialize('json', [comment_data, ])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            return HttpResponse(data, content_type='application/json')
        except:
            response = json.dumps([{ 'Info': 'Comment could not be added because there is no such movie ID in our database!'}])
            return HttpResponse(response, content_type='application/json')


@csrf_exempt
def top(request):
    if request.method == 'GET':
        try:
            start_date=request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            comment = Comment.objects.filter(date__range=[start_date, end_date])
            comment = comment.values('movie_id').annotate(total_comments=Count('movie_id'))
            comment=comment.order_by('-total_comments')
            data = list(comment)
            a = {}
            rank = 1
            for item in data:
                num = item['total_comments']
                if num not in a:
                   a[num] = rank
                   item.update({'rank':rank})
                   rank = rank + 1
                else:
                    item.update({'rank':rank-1})
            print(a)
            print(len(data))
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)
            response = json.dumps([{'Error': ' date range is required & must be in the format : YYYY-MM-DD '}])
            return HttpResponse(response, content_type='application/json')