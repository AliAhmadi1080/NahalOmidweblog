from blog.models import Blog, Comment, Consultation, Subscriber
from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
# Create your views here.


def aboutpage(request):
    return render(request, 'pages/about.html')


def contactpage(request):
    if request.method == 'POST':
        if request.POST['email'].strip() != '' and\
                request.POST['text'].strip != '':
            subject = f'Fatemeh site-contact masege from \
                {request.POST["email"]}'
            message = request.POST['text']
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, email_from, recipient_list,
                      fail_silently=False,
                      auth_user=None, auth_password=None,
                      connection=None, html_message=None)

    return render(request, 'pages/contact.html')


def homepage(request: HttpRequest):
    context = {'email':False}
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', False)
        full_name = request.POST.get('full_name', False)
        email = request.POST.get('email', False)
        if phone_number and full_name:
            try:
                consultation = Consultation.objects.create(
                    full_name=full_name, phone_number=phone_number)
                consultation.save()
            except:
                context['result'] = 'شماره تلفن شما درست نیست.'
                context['error'] = 'true'
            else:
                context['result'] = 'شما در لیست قرار گرفتید. با شما تماس گرفته خواهد شد.'
                context['error'] = 'false'
        elif email and full_name:
            context['email'] = True
            try:
                Subscriber.objects.create(
                    full_name=full_name, email=email)
            except:
                context['result'] = 'ایمیل واردشده نامعتبر است یا قبلاً در سیستم ثبت شده است.'
                context['error'] = 'true'
            else:
                context['result'] = 'ایمیل شما با موفقیت ثبت شد. از این پس درباره مطالب جدید به شما اطلاع‌رسانی خواهد شد. '
                context['error'] = 'false'

    return render(request, 'pages/home.html', context=context)


def detaleblog(request, pk):
    a = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        comment = Comment(
            blog=a, text=request.POST['text'], name=request.POST['name'])
        comment.save()

    b = Comment.objects.all().filter(blog=a, status='published')

    return render(request, 'pages/blogdetaile.html',
                  {'blogdetale': a, 'comments': b})


def allblog(request: HttpRequest):
    parameter = request.GET.get("blogtitle", '')
    allblogs = Blog.objects.filter(
        Q(titel__contains=parameter) | Q(sub_titel__contains=parameter))
    context = {'bloglist': allblogs}
    return render(request, 'pages/bloglist.html', context)
