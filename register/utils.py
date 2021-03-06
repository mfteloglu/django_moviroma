from .models import YonetmenDetay,FilmDetay,likedmovies,likeddirectors,AuthUser,Followers
from django.db.models import Q
from collections import Counter 
#from django.contrib.auth.models import User

def get_everything_as_array():
    everything = []
    for item in YonetmenDetay.objects.all():
        everything.append(item)
    for item in FilmDetay.objects.all():
        everything.append(item)
    for item in AuthUser.objects.all():
        everything.append(item)
    return everything

def countDistinct(arr): 
    return len(Counter(arr).keys()) 

def most_common(lst):
    return max(set(lst), key=lst.count)
    
def find_popular_movies(howmany):
    all_liked_movies = ""
    for item in likedmovies.objects.all():
        all_liked_movies += item.movies

    all_liked_movies_array = all_liked_movies.split(',')
    all_liked_movies_array.remove('')

    popular_movies = []

    if countDistinct(all_liked_movies_array) > howmany :
        for i in range(0,howmany):
            popular_movies.append(most_common(all_liked_movies_array))
            all_liked_movies_array = [x for x in all_liked_movies_array if x != most_common(all_liked_movies_array)]
    else :
        for i in range(0,countDistinct(all_liked_movies_array)):
            popular_movies.append(most_common(all_liked_movies_array))
            all_liked_movies_array = [x for x in all_liked_movies_array if x != most_common(all_liked_movies_array)]

    return popular_movies


def find_popular_directors(howmany):
    all_liked_directors = ""
    for item in likeddirectors.objects.all():
        all_liked_directors += item.directors

    all_liked_directors_array = all_liked_directors.split(',')
    all_liked_directors_array.remove('')

    popular_directors = []

    if countDistinct(all_liked_directors_array) > howmany :
        for i in range(0,howmany):
            popular_directors.append(most_common(all_liked_directors_array))
            all_liked_directors_array = [x for x in all_liked_directors_array if x != most_common(all_liked_directors_array)]
    else :
        for i in range(0,countDistinct(all_liked_directors_array)):
            popular_directors.append(most_common(all_liked_directors_array))
            all_liked_directors_array = [x for x in all_liked_directors_array if x != most_common(all_liked_directors_array)]


    return popular_directors

def find_followers_of_user(whichuser):
    all_followers = []
    for item in Followers.objects.all():
        if whichuser in item.followed:
            all_followers.append(AuthUser.objects.filter(id=item.user_id).first().username)

    return all_followers


