from django.urls import path
# from authapp.views import
from authapp.views import login, register, logout, profile

app_name = 'authapp'
urlpatterns = [

    # path('login/', login, name='login'),
    # path('register/', register, name='register'),
    # path('profile/', profile, name='profile'),
    # path('logout/', logout, name='logout'),

    path('login/', login.as_view(), name='login'),
    path('register/', register.as_view(), name='register'),
    path('profile/', profile.as_view(), name='profile'),
    path('logout/', logout.as_view(), name='logout'),

]
