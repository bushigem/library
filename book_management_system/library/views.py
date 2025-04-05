from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db import models
from .models import Book, BorrowRecord, Category, Location
from users.models import CustomUser  # 修改为从 users 应用导入 CustomUser

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'library/book_detail.html', {'book': book})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.available_quantity <= 0:
        messages.error(request, '该书已无可借数量')
        return redirect('book_detail', book_id=book_id)

    # 设置默认借阅期限为30天
    due_date = timezone.now() + timedelta(days=30)
    
    BorrowRecord.objects.create(
        user=request.user,
        book=book,
        due_date=due_date,
        status='borrowed'
    )

    book.available_quantity -= 1
    book.save()

    messages.success(request, f'成功借阅《{book.title}》')
    return redirect('book_detail', book_id=book_id)

@login_required
def return_book(request, borrow_id):
    borrow_record = get_object_or_404(BorrowRecord, pk=borrow_id)
    
    if borrow_record.user != request.user and not request.user.is_staff:
        messages.error(request, '您没有权限执行此操作')
        return redirect('my_borrows')

    if borrow_record.status == 'returned':
        messages.error(request, '该书已经归还')
        return redirect('my_borrows')

    borrow_record.return_date = timezone.now()
    borrow_record.status = 'returned'
    borrow_record.save()

    book = borrow_record.book
    book.available_quantity += 1
    book.save()

    messages.success(request, f'成功归还《{book.title}》')
    return redirect('my_borrows')

@login_required
def my_borrows(request):
    borrows = BorrowRecord.objects.filter(user=request.user).order_by('-borrow_date')
    return render(request, 'library/my_borrows.html', {'borrows': borrows})

# 管理员视图
@login_required
def manage_books(request):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面')
        return redirect('book_list')
    
    books = Book.objects.all()
    return render(request, 'library/manage_books.html', {'books': books})

@login_required
def manage_users(request):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面')
        return redirect('book_list')
    
    users = CustomUser.objects.all()  # 修改为使用 CustomUser
    return render(request, 'library/manage_users.html', {'users': users})

@login_required
def search_books(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(isbn__icontains=query)
        )
    
    if category:
        books = books.filter(category_id=category)
    
    categories = Category.objects.all()
    return render(request, 'library/search_books.html', {
        'books': books,
        'categories': categories,
        'query': query,
        'selected_category': category
    })

@login_required
def user_profile(request):
    if request.method == 'POST':
        # 处理用户信息更新
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, '个人信息更新成功')
        return redirect('user_profile')
    
    return render(request, 'library/user_profile.html', {
        'user': request.user
    })
