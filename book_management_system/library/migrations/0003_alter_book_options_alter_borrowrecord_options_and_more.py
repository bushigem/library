# Generated by Django 5.2 on 2025-04-04 14:15

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_location_options_remove_location_code_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': '图书', 'verbose_name_plural': '图书'},
        ),
        migrations.AlterModelOptions(
            name='borrowrecord',
            options={'verbose_name': '借阅记录', 'verbose_name_plural': '借阅记录'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '图书分类', 'verbose_name_plural': '图书分类'},
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=255, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='book',
            name='available_quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='可借数量'),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='library.category', verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_image_url',
            field=models.URLField(blank=True, max_length=2083, null=True, verbose_name='封面图片'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=20, unique=True, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='book',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='library.location', verbose_name='馆藏位置'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_date',
            field=models.DateField(blank=True, null=True, verbose_name='出版日期'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='出版社'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=255, verbose_name='书名'),
        ),
        migrations.AlterField(
            model_name='book',
            name='total_quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='总数量'),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='library.book', verbose_name='图书'),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='borrow_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='借阅日期'),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='due_date',
            field=models.DateTimeField(verbose_name='应还日期'),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='return_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='归还日期'),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='status',
            field=models.CharField(choices=[('borrowed', '已借出'), ('returned', '已归还'), ('overdue', '逾期'), ('pending', '待处理')], default='borrowed', max_length=10, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='分类名称'),
        ),
    ]
