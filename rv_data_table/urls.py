from django.contrib import admin
from django.urls import path
from .views import home,signup,verify,login_view

urlpatterns = [
   path('', home,name='home'),
    path('signup/', signup, name='signup'),
    path('verify/<int:user_id>/', verify, name='verify'),
    path('login/', login_view, name='login'),
]