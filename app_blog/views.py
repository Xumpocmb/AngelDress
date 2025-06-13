from django.shortcuts import render

def blog_view(request):
    return render(request, 'app_blog/blog.html')
