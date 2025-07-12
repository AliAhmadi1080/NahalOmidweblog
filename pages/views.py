from django.shortcuts import render, get_object_or_404
from blog.models import Blog, Comment
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


def aboutpage(request):
    return render(request, 'pages/about.html')


def contactpage(request):
    if request.method == 'POST':
        if request.POST['email'].strip() != '' and request.POST['text'].strip != '':

            print(request.POST)

            subject = f'Fatemeh site-contact masege from {request.POST["email"]}'
            message = request.POST['text']
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False,
                      auth_user=None, auth_password=None, connection=None, html_message=None)

    return render(request, 'pages/contact.html')


def homepage(request):
    a = Blog.objects.all()[:5]
    return render(request, 'pages/home.html', {'blogs': a})


def detaleblog(request, pk):
    a = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        comment = Comment(
            blog=a, text=request.POST['text'], name=request.POST['name'])
        print(comment)
        comment.save()

    b = Comment.objects.all().filter(blog=a, status='published')

    return render(request, 'pages/blogdetaile.html', {'blogdetale': a, 'comments': b})


def allblog(request):
    a = Blog.objects.all()
    context = {'bloglist': a}
    print(a, context)
    return render(request, 'pages/bloglist.html', context)
