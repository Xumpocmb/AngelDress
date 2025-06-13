from django.shortcuts import render

def news_view(request):
    return render(request, 'app_news/news.html')
