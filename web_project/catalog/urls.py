from django.urls import path
from . import views


app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.author_detail_view, name='author-detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),

    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<uuid:pk>/renew/', views.renew_book_staff, name='renew-book-staff'),
    
    path('contact/', views.contact_email, name='contact'),
    path('contact_email_sent/', views.contact_email_sent, name='contact_email_sent'),
    
    path('mybooks/', views.BorrowedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allbooks/', views.BorrowedBooksByStaffListView.as_view(), name='all-borrowed'),

] 