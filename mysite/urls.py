"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from register import views as v



urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path("register/", v.register, name="register"),
    path("", v.index, name="index"),
    path('login/', v.login_view, name='login'),
    path('home/', v.home,name="home"),
    path('logout/', v.logout_view, name="logout"),
    path('directors/<int:id>/', v.director_view,name="directorview"),
    path('movies/<int:id>/', v.movie_view ,name="movieview"),
    path('users/<int:id>/', v.user_view,name="userview"),
    path('search/',v.searchdirector,name="search"),
    path('searchmovie/',v.searchmovie,name="searchmovie"),
    path('searchuser/',v.searchuser,name="searchuser"),
    path('directors/<int:id>/<int:id1>/lm',v.likemovie,name="likemovie"),
    path('directors/<int:id>/<int:id1>/um',v.unlikemovie,name="unlikemovie"),
    path('directors/ld/<int:id>',v.likedirector,name="likedirector"),
    path('directors/ud/<int:id>',v.unlikedirector,name="unlikedirector"),
    path('users/fu/<int:id>',v.follow_user,name="followuser"),
    path('users/uu/<int:id>',v.unfollow_user,name="unfollowuser")
]
