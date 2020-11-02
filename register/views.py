# views.py
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import YonetmenDetay,FilmDetay,likedmovies,likeddirectors,AuthUser,Followers
from django.db.models import Q
from django.contrib.auth.models import User
from register.utils import get_everything_as_array,find_popular_movies,find_popular_directors
import json
from django.core import serializers

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/login")
    else:
        form = RegisterForm()

    return render(request, "moviroma/home-signup.html", {"form":form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request,user)
            return redirect("/home")
    else:
        form = AuthenticationForm()
    return render(request, "moviroma/home-login.html", {"form": form})

def logout_view(request):
    logout(request)
    form = AuthenticationForm(data=request.POST)
    return redirect("/login")



def index(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        return redirect("/home")

def home(request):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        current_user_1 = AuthUser.objects.filter(username=current_user.username).first()

        popular_movies_on_moviroma = []
        for item in find_popular_movies(9):
            popular_movies_on_moviroma.append(FilmDetay.objects.filter(film_title=item).first())

        popular_directors_on_moviroma = []
        for item in find_popular_directors(9):
            popular_directors_on_moviroma.append(YonetmenDetay.objects.filter(yonetmen_ad=item).first())

        context = {'popularmovies': popular_movies_on_moviroma,'populardirectors': popular_directors_on_moviroma ,'currentuser': current_user_1}
        return render(request,"moviroma/home.html",context)       

def director_view(request,id):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        current_user_1 = AuthUser.objects.filter(username=current_user.username).first()

        if likedmovies.objects.filter(user=current_user).count() != 0:
            playlist = likedmovies.objects.filter(user=current_user).first()
        else:
            playlist = likedmovies(movies="",user=current_user)
            playlist.save()

        if likeddirectors.objects.filter(user=current_user).count() != 0:
            playlist1 = likeddirectors.objects.filter(user=current_user).first()
        else:
            playlist1 = likeddirectors(directors="",user=current_user)
            playlist1.save()
     
        selecteddirector = YonetmenDetay.objects.filter(yonetmen_tmdb_id=id).first()
        directorsmovies = FilmDetay.objects.filter(yonetmen_id=id).distinct()
        sorteddirectorsmovies = directorsmovies.order_by('-film_tmdb_rating')

        directorsmoviesdates = []
        for item in directorsmovies:
            if item.film_yayinlanma_tarihi:
                directorsmoviesdates.append(item.startdate_as_date())

        latest = directorsmoviesdates[0]
        for item in directorsmoviesdates:
            if item > latest:
                latest = item
            
        for item in directorsmovies:
            if item.film_yayinlanma_tarihi:
                if item.startdate_as_date()==latest:
                    latestmovie = item

        #everything1 = json.dumps(get_everything_as_array())
        everything1 = serializers.serialize('json',YonetmenDetay.objects.all())

        context = {'person': selecteddirector,'movies': sorteddirectorsmovies, 'latestmovie': latestmovie, 'likedmovies': playlist.movies, 'likeddirectors': playlist1.directors,'currentuser': current_user_1,'everything': everything1}
        
        
        return render(request,"moviroma/yonetmen_main_page.html",context)

def movie_view(request,id):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        current_user_1 = AuthUser.objects.filter(username=current_user.username).first()
        if likedmovies.objects.filter(user=current_user).count() != 0:
            playlist = likedmovies.objects.filter(user=current_user).first()
        else:
            playlist = likedmovies(movies="",user=current_user)
            playlist.save()        

        selected_movie = FilmDetay.objects.filter(film_tmdb_id=id).first()
        movies_director = YonetmenDetay.objects.filter(yonetmen_tmdb_id=selected_movie.yonetmen_id).first()
        selected_movie_trailers = selected_movie.film_video_link.split(',') 
        selected_movie_images = selected_movie.movie_images_link.split(',')
        selected_movie_similars_id = selected_movie.recomendation_movie_id.split(',')

        selected_movie_similars = []
        for item in selected_movie_similars_id:
            if FilmDetay.objects.filter(film_tmdb_id=item).first():
                selected_movie_similars.append(FilmDetay.objects.filter(film_tmdb_id=item).first())

        context = {'movie': selected_movie, 'director': movies_director, 'trailer': selected_movie_trailers[0], 'images': selected_movie_images, 'similars': selected_movie_similars[:5], 'likedmovies': playlist.movies,'currentuser': current_user_1}
        return render(request,"moviroma/film_page.html",context)

def user_view(request,id):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        current_user_1 = AuthUser.objects.filter(username=current_user.username).first()

        if likedmovies.objects.filter(user=current_user).count() != 0:
            playlist = likedmovies.objects.filter(user=current_user).first()
        else:
            playlist = likedmovies(movies="",user=current_user)
            playlist.save()

        if likeddirectors.objects.filter(user=current_user).count() != 0:
            playlist1 = likeddirectors.objects.filter(user=current_user).first()
        else:
            playlist1 = likeddirectors(directors="",user=current_user)
            playlist1.save()

        if Followers.objects.filter(user=current_user).count() != 0:
            playlist2 = Followers.objects.filter(user=current_user).first()
        else:
            playlist2 = Followers(followed="",user=current_user)
            playlist2.save()
     
        selected_person = AuthUser.objects.filter(id=id).first()
        selected_person_liked_movies = likedmovies.objects.filter(user=User.objects.filter(username=selected_person.username).first()).first()
        selected_person_liked_movies_1 = selected_person_liked_movies.movies.split(',')
        selected_person_liked_movies_2 =[]
        for item in selected_person_liked_movies_1:
            if FilmDetay.objects.filter(film_title=item).first():
                selected_person_liked_movies_2.append(FilmDetay.objects.filter(film_title=item).first())

        selected_person_liked_directors = likeddirectors.objects.filter(user=User.objects.filter(username=selected_person.username).first()).first()
        selected_person_liked_directors_1 = selected_person_liked_directors.directors.split(',')
        selected_person_liked_directors_2 =[]
        for item in selected_person_liked_directors_1:
            if YonetmenDetay.objects.filter(yonetmen_ad=item).first():
                selected_person_liked_directors_2.append(YonetmenDetay.objects.filter(yonetmen_ad=item).first())

        context = {'person': selected_person,'likedmovies': playlist.movies, 'likeddirectors': playlist1.directors,'selectedpersonlikedmovies': selected_person_liked_movies_2,'selectedpersonlikeddirectors': selected_person_liked_directors_2,'selectedpersonfollowedusers': playlist2.followed,'currentuser': current_user_1}
        return render(request,"moviroma/user_page.html",context)

def searchdirector(request):
    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
            queryset1 = (Q(yonetmen_ad__icontains=query))
            queryset2 = (Q(film_title__icontains=query))
            queryset3 = (Q(username__icontains=query))

            current_user = request.user
            current_user_1 = AuthUser.objects.filter(username=current_user.username).first()
            #I assume "text" is a field in your model
            #i.e., text = model.TextField()
            #Use | if searching multiple fields, i.e., 
            #queryset = (Q(text__icontains=query))|(Q(other__icontains=query))
            #results = director.objects.filter(queryset).distinct()
            results = YonetmenDetay.objects.filter(queryset1).distinct()
            numberofresultsdirector = YonetmenDetay.objects.filter(queryset1).distinct().count()            
            numberofresultsmovie = FilmDetay.objects.filter(queryset2).distinct().count()
            numberofresultsuser = AuthUser.objects.filter(queryset3).distinct().count()

            context = {'searchedperson': results,'numberofsearcheduser': numberofresultsuser, 'numberofsearchedperson': numberofresultsdirector,'numberofsearchedmovie': numberofresultsmovie,'search': query,'currentuser': current_user_1}
    else:
       results= []
       numberofresults = 0
       numberofresultsmovie = 0
       numberofresultsdirector = 0

       context = {'searchedperson': results,'numberofsearchedperson': numberofresultsdirector,'numberofsearchedmovie': numberofresultsmovie,'search': query}
    return render(request, "moviroma/searchdirector.html", context)

def searchuser(request):
    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
            queryset1 = (Q(yonetmen_ad__icontains=query))
            queryset2 = (Q(film_title__icontains=query))
            queryset3 = (Q(username__icontains=query))

            current_user = request.user
            current_user_1 = AuthUser.objects.filter(username=current_user.username).first()
            #I assume "text" is a field in your model
            #i.e., text = model.TextField()
            #Use | if searching multiple fields, i.e., 
            #queryset = (Q(text__icontains=query))|(Q(other__icontains=query))
            #results = director.objects.filter(queryset).distinct()
            results = AuthUser.objects.filter(queryset3).distinct()
            numberofresultsdirector = YonetmenDetay.objects.filter(queryset1).distinct().count()
            numberofresultsmovie = FilmDetay.objects.filter(queryset2).distinct().count()
            numberofresultsuser = AuthUser.objects.filter(queryset3).distinct().count()

            context = {'searcheduser': results,'numberofsearcheduser': numberofresultsuser,'numberofsearchedperson': numberofresultsdirector,'numberofsearchedmovie': numberofresultsmovie,'search': query,'currentuser': current_user_1}
    else:
       results= []
       numberofresults = 0
       numberofresultsmovie = 0

       context = {'searchedperson': results,'numberofsearchedperson': numberofresultsdirector,'numberofsearchedmovie': numberofresultsmovie,'search': query}
    return render(request, "moviroma/searchuser.html", context)

def searchmovie(request):
    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
            queryset1 = (Q(yonetmen_ad__icontains=query))
            queryset2 = (Q(film_title__icontains=query))
            queryset3 = (Q(username__icontains=query))

            current_user = request.user
            current_user_1 = AuthUser.objects.filter(username=current_user.username).first()            
            #I assume "text" is a field in your model
            #i.e., text = model.TextField()
            #Use | if searching multiple fields, i.e., 
            #queryset = (Q(text__icontains=query))|(Q(other__icontains=query))
            #results = director.objects.filter(queryset).distinct()
            results = FilmDetay.objects.filter(queryset2).distinct()
            numberofresultsmovie = FilmDetay.objects.filter(queryset2).distinct().count()
            numberofresultsdirector = YonetmenDetay.objects.filter(queryset1).distinct().count()
            numberofresultsuser = AuthUser.objects.filter(queryset3).distinct().count()

            context = {'searchedmovie': results,'numberofsearcheduser': numberofresultsuser,'numberofsearchedmovie': numberofresultsmovie,'numberofsearchedperson': numberofresultsdirector,'search': query,'currentuser': current_user_1}
    else:
       results = []
       numberofresults = 0
       context = {'searchedmovie': results,'numberofsearchedmovie': numberofresultsmovie,'numberofsearchedperson': numberofresultsdirector,'search': query}
    return render(request, "moviroma/searchmovie.html", context)

def likemovie(request,id,id1):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        liked_movie = FilmDetay.objects.filter(film_tmdb_id=id1).first()
        if likedmovies.objects.filter(user=current_user).count() == 0:
            likedmovies(user=current_user,movies=liked_movie).save()
        else:
            playlist = likedmovies.objects.filter(user=current_user).first()
            playlist.movies += "," + liked_movie.film_title
            playlist.save()
                   
        #return director_view(request,id)
        return redirect(request.META['HTTP_REFERER'])

def unlikemovie(request,id,id1):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        unliked_movie = FilmDetay.objects.filter(film_tmdb_id=id1).first()

        playlist = likedmovies.objects.filter(user=current_user).first()
        playlist.movies = playlist.movies.replace(","+ unliked_movie.film_title,"")
        playlist.save()
                   
        #return director_view(request,id)  
        return redirect(request.META['HTTP_REFERER'])
          


def likedirector(request,id):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        liked_director = YonetmenDetay.objects.filter(yonetmen_tmdb_id=id).first()
        if likeddirectors.objects.filter(user=current_user).count() == 0:
            likeddirectors(user=current_user,directors=liked_director).save()
        else:
            playlist = likeddirectors.objects.filter(user=current_user).first()
            playlist.directors += "," + liked_director.yonetmen_ad
            playlist.save()
                   
        #return director_view(request,id)
        return redirect(request.META['HTTP_REFERER'])

def unlikedirector(request,id):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        unliked_director = YonetmenDetay.objects.filter(yonetmen_tmdb_id=id).first()

        playlist = likeddirectors.objects.filter(user=current_user).first()
        playlist.directors = playlist.directors.replace(","+ unliked_director.yonetmen_ad,"")
        playlist.save()
                   
        #return director_view(request,id)  
        return redirect(request.META['HTTP_REFERER'])
        
def follow_user(request,id):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        liked_user = AuthUser.objects.filter(id=id).first()
        if Followers.objects.filter(user=current_user).count() == 0:
            Followers(user=current_user,directors=liked_user.username).save()
        else:
            followlist = Followers.objects.filter(user=current_user).first()
            followlist.followed += "," + liked_user.username
            followlist.save()
                   
        #return director_view(request,id)
        return redirect(request.META['HTTP_REFERER'])

def unfollow_user(request,id):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        unliked_user = AuthUser.objects.filter(id=id).first()

        followlist = Followers.objects.filter(user=current_user).first()
        followlist.followed = followlist.followed.replace(","+ unliked_user.username,"")
        followlist.save()
                   
        #return director_view(request,id)  
        return redirect(request.META['HTTP_REFERER'])