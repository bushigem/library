from django.contrib import admin
from .models import Book, BorrowRecord, Category, Location

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'total_quantity', 'available_quantity')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category',)
    
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'return_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')
    
    class Meta:
        verbose_name = '借阅记录'
        verbose_name_plural = '借阅记录'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    
    class Meta:
        verbose_name = '图书分类'
        verbose_name_plural = '图书分类'

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'description')  # 修改这里
    search_fields = ('location_name',)  # 修改这里
    
    class Meta:
        verbose_name = '馆藏位置'
        verbose_name_plural = '馆藏位置'
