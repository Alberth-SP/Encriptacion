from django.urls import re_path, include,path
from . import views

urlpatterns = [
    path('', views.getPage),
    path('/cipher', views.cipher,name="cipher"),
    path('/descipher', views.descipher,name="descipher"),
    path('/down_key', views.down_key,name="down_key"),
    path('/down_cipher', views.down_cipher,name="down_cipher"),
    path('/down_descipher', views.down_descipher,name="down_descipher"),

]
