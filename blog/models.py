from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models


class Categorys(models.Model):
    name = models.CharField(max_length=60, verbose_name='اسم عنوان')

    def __str__(self) -> str:
        return self.name


class Blog(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='نویسنده')
    titel = models.CharField(max_length=60, verbose_name='عنوان')
    sub_titel = models.CharField(max_length=150, verbose_name='زیر عنوان')
    image = models.ImageField(
        verbose_name='عکس', upload_to='statics\assets\img\\',
        default='statics\assets\img\about-bg.jpg')
    date = models.DateField(
        auto_created=True, auto_now_add=True, verbose_name='زمان')
    categorys = models.ManyToManyField('Categorys', verbose_name='دسته بندی')
    text = models.TextField(verbose_name='متن اصلی')
    like_count = models.PositiveIntegerField(
        default=0, auto_created=True, verbose_name='تعداد لایک')

    def __str__(self) -> str:
        return f'{self.author} , {self.titel}'

    def get_absolute_url(self):
        return reverse('detaileblog', args=[str(self.pk)])


class Comment(models.Model):
    STATUS_CHOICES = (
        ('checking', 'درحال بررسی'),
        ('rejected', 'رد شده'),
        ('published', 'پذیرفته شده')
    )
    status = models.CharField(max_length=9,
                              choices=STATUS_CHOICES,
                              default='checking', verbose_name='وضعیت')
    name = models.CharField(max_length=32, verbose_name='نام نویسنده')
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, verbose_name='مطلب')
    text = models.TextField(verbose_name='محتوا')

    def __str__(self) -> str:
        return f'{self.blog.titel}'


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, verbose_name='مطلب')
    is_liked = models.BooleanField(default=False, verbose_name='لایک شده؟')

    def __str__(self) -> str:
        return f'{self.user} -> {self.is_liked}'


class Consultation(models.Model):
    STATUS_CHOICES = (
        ('unreaded', 'خوانده نشده'),
        ('rejected', 'رد شده'),
        ('accepted', 'پذیرفته شده')
    )
    full_name = models.CharField(
        max_length=32, verbose_name='نام و نام خانوادگی')
    phone_number = phone_number = models.CharField(
        max_length=11,
        verbose_name='شماره تلفن',
        validators=[RegexValidator(regex=r'^09\d{9}$',
                                   message='شماره تلفن میبایست به شکل 09123456789 باشد')])
    status = models.CharField(max_length=9,
                              choices=STATUS_CHOICES,
                              default='unreaded', verbose_name='وضعیت')

    def __str__(self):
        return f'{self.full_name}, {self.phone_number}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Subscriber(models.Model):
    full_name = models.CharField(
        max_length=32, verbose_name='نام و نام خانوادگی')
    email = models.CharField(
        max_length=254,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            message='لطفاً یک آدرس ایمیل معتبر وارد کنید.'
        )],
        unique=True,
        verbose_name='ایمیل'
    )

    def __str__(self):
        return f'{self.full_name}, {self.email}'

    def save(self, *args, **kwargs):
        self.full_clean()
        self.email = self.email.replace('.', '')
        return super().save(*args, **kwargs)
