from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('borrow/<int:borrow_id>/return/', views.return_book, name='return_book'),
    path('my-borrows/', views.my_borrows, name='my_borrows'),
    path('manage/books/', views.manage_books, name='manage_books'),
    path('manage/users/', views.manage_users, name='manage_users'),
    path('search/', views.search_books, name='search_books'),  # 添加这行
    path('profile/', views.user_profile, name='user_profile'),
]