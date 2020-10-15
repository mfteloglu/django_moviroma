# from django.db import models

# class director(models.Model):
#     yonetmen_tmdb_id  = models.TextField(default='')
#     yonetmen_imdb_id  = models.TextField(default='')
#     yonetmen_ad  = models.TextField(max_length=140, default='')
#     yonetmen_dogum  = models.TextField(default='')
#     yonetmen_olum  = models.TextField(default=''),
#     yonetmen_biyografi  = models.TextField(default='')
#     yonetmen_dogum_yeri  = models.TextField(default='')
#     yonetmen_pp_linki  = models.TextField(default='')  

#     def __str__(self):
#         return self.yonetmen_ad

# # Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime as dt

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FilmDetay(models.Model):
    yonetmen_id = models.TextField()
    film_tmdb_id = models.TextField(primary_key=True)
    film_imdb_id = models.TextField()
    film_title = models.TextField()
    film_original_title = models.TextField()
    film_aciklamasi = models.TextField()
    film_turu = models.TextField()
    film_poster_linki = models.TextField()
    film_backdrop_linki = models.TextField()
    film_yayinlanma_tarihi = models.TextField()
    film_suresi = models.TextField()
    film_tmdb_rating = models.TextField()

    class Meta:
        managed = False
        db_table = 'film_detay'

    def __str__(self):
        return self.film_title
        
    def startdate_as_date(self):
        return dt.strptime(self.film_yayinlanma_tarihi,'%Y-%m-%d')

class PollsChoice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField()
    question = models.ForeignKey('PollsQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'polls_choice'


class PollsQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'polls_question'


class RegisterDirector(models.Model):
    yonetmen_ad = models.TextField()
    yonetmen_biyografi = models.TextField()
    yonetmen_dogum = models.TextField()
    yonetmen_dogum_yeri = models.TextField()
    yonetmen_imdb_id = models.TextField()
    yonetmen_pp_linki = models.TextField()
    yonetmen_tmdb_id = models.TextField()

    class Meta:
        managed = False
        db_table = 'register_director'


class YonetmenDetay(models.Model):
    yonetmen_tmdb_id = models.TextField(primary_key=True)
    yonetmen_imdb_id = models.TextField()
    yonetmen_ad = models.TextField()
    yonetmen_dogum = models.TextField()
    yonetmen_olum = models.TextField()
    yonetmen_biyografi = models.TextField()
    yonetmen_dogum_yeri = models.TextField()
    yonetmen_pp_linki = models.TextField()

    class Meta:
        managed = False
        db_table = 'yonetmen_detay'

    def __str__(self):
        return self.yonetmen_ad


