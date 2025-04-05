from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Book, BorrowRecord
from django.utils import timezone
from datetime import timedelta

@login_required
def book_list(request):
    query = request.GET.get('query', '')
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(isbn__icontains=query) |
            models.Q(category__name__icontains=query)
        )
    
    return render(request, 'library/book_list.html', {
        'books': books,
        'query': query
    })

@login_required
def my_borrows(request):
    borrows = BorrowRecord.objects.filter(user=request.user).exclude(status='returned')
    for borrow in borrows:
        borrow.can_renew = not borrow.is_overdue() and borrow.status == 'borrowed'
    return render(request, 'library/my_borrows.html', {'borrows': borrows})

@login_required
def renew_book(request, borrow_id):
    borrow = get_object_or_404(BorrowRecord, id=borrow_id, user=request.user)
    if borrow.status == 'borrowed' and not borrow.is_overdue():
        borrow.due_date = borrow.due_date + timedelta(days=30)
        borrow.save()
        messages.success(request, f'《{borrow.book.title}》续借成功，新的归还日期为 {borrow.due_date.strftime("%Y-%m-%d")}')
    else:
        messages.error(request, '该书不可续借')
    return redirect('my_borrows')

@login_required
def borrow_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        
        # 检查是否有相同未还的书
        existing_borrow = BorrowRecord.objects.filter(
            user=request.user,
            book=book,
            status='borrowed'
        ).exists()
        
        if existing_borrow:
            messages.error(request, '您已借阅过这本书且尚未归还')
            return redirect('book_list')
            
        if book.available_quantity > 0:
            due_date = timezone.now() + timedelta(days=30)
            BorrowRecord.objects.create(
                user=request.user,
                book=book,
                due_date=due_date,
                status='borrowed'
            )
            book.available_quantity -= 1
            book.save()
            messages.success(request, f'成功借阅《{book.title}》，请在 {due_date.strftime("%Y-%m-%d")} 前归还')
        else:
            messages.error(request, '该书已无可借数量')
    return redirect('book_list')

@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(BorrowRecord, id=borrow_id, user=request.user)
    if borrow.status == 'borrowed' or borrow.status == 'overdue':
        borrow.status = 'returned'
        borrow.return_date = timezone.now()
        borrow.save()
        book = borrow.book
        book.available_quantity += 1
        book.save()
        messages.success(request, f'成功归还《{book.title}》')
    return redirect('my_borrows')

@login_required
@user_passes_test(lambda u: u.is_staff)  # 确保只有管理员可以访问
def manage_books(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'library/manage_books.html', {'books': books})
