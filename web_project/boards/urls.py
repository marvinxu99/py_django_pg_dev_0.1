from django.urls import path

from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.boards_home, name='boards_home'),
    path('<int:board_id>/', views.board_topics, name='board_topics'),
    path('<int:board_id>/new', views.new_topic, name='new_topic'),
   
]
