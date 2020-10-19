# views.py
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import YonetmenDetay,FilmDetay,likedmovies
from django.db.models import Q

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
            return redirect("/index")
    else:
        form = AuthenticationForm()
    return render(request, "moviroma/home-login.html", {"form": form})

def logout_view(request):
    logout(request)
    form = AuthenticationForm(data=request.POST)
    return redirect("/login")



def index(request):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        return render(request,"moviroma/yonetmen_main_page.html")


def director_view(request,id):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user

        if likedmovies.objects.filter(user=current_user).count() != 0:
            playlist = likedmovies.objects.filter(user=current_user).first()
        else:
            playlist = likedmovies(movies="",user=current_user)
            playlist.save()
     
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
        context = {'person': selecteddirector,'movies': sorteddirectorsmovies, 'latestmovie': latestmovie, 'likedmovies': playlist.movies}
        return render(request,"moviroma/yonetmen_main_page.html",context)

def searchdirector(request):
    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
            queryset1 = (Q(yonetmen_ad__icontains=query))
            queryset2 = (Q(film_title__icontains=query))
            #I assume "text" is a field in your model
            #i.e., text = model.TextField()
            #Use | if searching multiple fields, i.e., 
            #queryset = (Q(text__icontains=query))|(Q(other__icontains=query))
            #results = director.objects.filter(queryset).distinct()
            results = YonetmenDetay.objects.filter(queryset1).distinct()
            numberofresultsdirector = YonetmenDetay.objects.filter(queryset1).distinct().count()

            numberofresultsmovie = FilmDetay.objects.filter(queryset2).distinct().count()

            context = {'searchedperson': results,'numberofsearchedperson': numberofresultsdirector,'numberofsearchedmovie': numberofresultsmovie,'search': query}
    else:
       results= []
       numberofresults = 0
       numberofresultsmovie = 0

       context = {'searchedperson': results,'numberofsearchedperson': numberofresultsdirector,'numberofsearchedmovie': numberofresultsmovie,'search': query}
    return render(request, "moviroma/searchdirector.html", context)

def searchmovie(request):
    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
            queryset1 = (Q(yonetmen_ad__icontains=query))
            queryset2 = (Q(film_title__icontains=query))
            
            #I assume "text" is a field in your model
            #i.e., text = model.TextField()
            #Use | if searching multiple fields, i.e., 
            #queryset = (Q(text__icontains=query))|(Q(other__icontains=query))
            #results = director.objects.filter(queryset).distinct()
            results = FilmDetay.objects.filter(queryset2).distinct()
            numberofresultsmovie = FilmDetay.objects.filter(queryset2).distinct().count()

            numberofresultsdirector = YonetmenDetay.objects.filter(queryset1).distinct().count()

            context = {'searchedmovie': results,'numberofsearchedmovie': numberofresultsmovie,'numberofsearchedperson': numberofresultsdirector,'search': query}
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
                   
        return director_view(request,id)

def unlikemovie(request,id,id1):
    if not request.user.is_authenticated:
        return render(request,"moviroma/404error.html")
    else:
        current_user = request.user
        unliked_movie = FilmDetay.objects.filter(film_tmdb_id=id1).first()

        playlist = likedmovies.objects.filter(user=current_user).first()
        playlist.movies = playlist.movies.replace(","+ unliked_movie.film_title,"")
        playlist.save()
                   
        return director_view(request,id)    
        

