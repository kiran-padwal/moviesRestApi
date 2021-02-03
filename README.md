#moviesRestApi
Restfull Api

1) Build with Docker-compose
    a) command : docker-compose up --build
    This will run the docker-compose.yml and install all dependencies and run the django server
    I have windows 8 OS, so i have installed docker toolbox, in order to run my application on browser
    i need to go on http://192.168.99.100:3000/movies to run the application on my browser
    i am currently running Docker on a Linux VM
    if you are running docker other than docker toolbox on linux vm then yours may be http://localhost:3000/movies

2) Manual installation without docker :
        a) pip3 install django
        b) pip3 install requests
           python version : 3.6
        c) python manage.py runserver
        d) on browser go on http:127.0.0.1:8000/movies

3) Endpoints :
      1 POST /movies to add movie with payload = {"title":"ironman"}
      2 GET /movies filters are optional and can be passed as query string
            for example /movies?genre=action
            GET /movies?movie_id=33
      3 POST /comments to add comment to particular movie id with payload = {"comment":"comment text","movie_id":"33"}
        here both are required post values
      4 GET /comments returns a list of all the comments in the database
      5 GET /comments?movie_id=33 will return all the comments on movie id = 33
      5 GET /top will return top movies based on the total number of comment in the particular date range
           if total number of comments are equal rank will be same
           required parameters are start_date & end_date
           eg: /top?start_date=2019-08-09&end_date=2019-08-10

4) App is deployed on pythonanywhere.com :
   a) url : http://kiranlocalbackup.pythonanywhere.com/movies

5) basic tests of endpoints are done
   a) to run the test using docker-compose :
      1) command : docker-compose build
      2) command : docker-compose run web python manage.py test
   b) to run the test without docker-compose:
      1) python manage.py test

6) github public repository : https://github.com/kiran-padwal-connecsi/moviesRestApi.git
