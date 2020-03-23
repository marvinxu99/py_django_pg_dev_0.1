from django.urls import path, re_path

from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.boards_home, name='boards_home'),
    path('<int:board_id>/new/', views.new_topic, name='new_topic'),
    path('<int:board_id>/', views.board_topics, name='board_topics'),
    path('<int:board_id>/topics/<int:topic_id>/', views.topic_posts, name='topic_posts'),  
    path('<int:board_id>/topics/<int:topic_id>/reply/', views.topic_reply, name='topic_reply'),
]
