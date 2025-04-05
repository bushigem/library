from django.db import models
from django.utils import timezone
from users.models import CustomUser  # 使用 users 应用中的 CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    description = models.TextField(null=True, blank=True, verbose_name='描述')

    class Meta:
        db_table = 'CATEGORY'
        verbose_name = '图书分类'
        verbose_name_plural = '图书分类'

    def __str__(self):
        return self.name

class Location(models.Model):
    location_name = models.CharField(max_length=100, verbose_name='位置名称', default='默认位置')
    description = models.TextField(blank=True, null=True, verbose_name='描述')

    class Meta:
        verbose_name = '馆藏位置'
        verbose_name_plural = '馆藏位置'

    def __str__(self):
        return self.location_name

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='书名')
    author = models.CharField(max_length=255, verbose_name='作者')
    isbn = models.CharField(max_length=20, unique=True, verbose_name='ISBN')
    publisher = models.CharField(max_length=150, null=True, blank=True, verbose_name='出版社')
    publication_date = models.DateField(null=True, blank=True, verbose_name='出版日期')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name='分类')
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, verbose_name='馆藏位置')
    total_quantity = models.PositiveIntegerField(default=1, verbose_name='总数量')
    available_quantity = models.PositiveIntegerField(default=1, verbose_name='可借数量')
    description = models.TextField(null=True, blank=True, verbose_name='描述')
    cover_image_url = models.URLField(max_length=2083, null=True, blank=True, verbose_name='封面图片')

    class Meta:
        db_table = 'BOOK'
        verbose_name = '图书'
        verbose_name_plural = '图书'

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_quantity > 0

    def can_borrow(self):
        return self.available_quantity > 0

class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('borrowed', '已借出'),
        ('returned', '已归还'),
        ('overdue', '逾期'),
        ('pending', '待处理')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, verbose_name='用户')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, verbose_name='图书')
    borrow_date = models.DateTimeField(default=timezone.now, verbose_name='借阅日期')
    due_date = models.DateTimeField(verbose_name='应还日期')
    return_date = models.DateTimeField(null=True, blank=True, verbose_name='归还日期')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed', verbose_name='状态')

    class Meta:
        db_table = 'BORROW_RECORD'
        verbose_name = '借阅记录'
        verbose_name_plural = '借阅记录'

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def is_overdue(self):
        if not self.return_date and timezone.now() > self.due_date:
            return True
        return False

    def get_fine_amount(self):
        if not self.is_overdue():
            return 0
        days_overdue = (timezone.now() - self.due_date).days
        return max(0, days_overdue * 0.5)  # 每天罚款0.5元
