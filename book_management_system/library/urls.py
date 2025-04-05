from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('my-borrows/', views.my_borrows, name='my_borrows'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('manage/', views.manage_books, name='manage_books'),  # 添加管理图书的URL
]