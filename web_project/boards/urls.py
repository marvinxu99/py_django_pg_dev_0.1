from django.urls import path, include

from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.boards_home, name='boards_home'),

    #path('contact/', views.contact_email, name='contact'),
    
]
