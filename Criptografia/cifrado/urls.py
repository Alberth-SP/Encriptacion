from django.urls import re_path, include,path
from . import views

urlpatterns = [
    path('', views.getPage),
    path('/cipher', views.cipher,name="cipher"),
    path('/descipher', views.descipher,name="descipher"),

]
