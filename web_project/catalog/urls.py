from django.urls import path
from . import views


app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.author_detail_view, name='author-detail'),
    path('contact/', views.contact_email, name='contact'),
    path('contact_email_sent/', views.contact_email_sent, name='contact_email_sent'),

] 