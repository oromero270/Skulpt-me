from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('adding', views.log_new_workout),
    path('login', views.security),
    path('submitinfo', views.creating),
    path('home', views.myhome),
    path('home/pretest', views.examnotes),
    path('logout', views.clearuser),
    path('test1', views.first_test),
    path('test2', views.second_test),
    path('test3', views.third_test),
    path('test4', views.final_test),
    path('sub1', views.first_sub),
    path('sub2', views.second_sub),
    path('sub3', views.third_sub),
    path('final', views.final_sub),
    path('home/stats', views.history),
    path('home/workout', views.prework),
    path('selections', views.sub_today_workout),
    path('add/workout', views.add_workout),
    path('work', views.begin_workout),
    path('Val', views.regval),
    
]