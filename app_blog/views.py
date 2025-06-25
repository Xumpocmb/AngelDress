from django.shortcuts import render, get_object_or_404

from app_blog.models import Post


def blog_view(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'app_blog/blog.html', context=context)


def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post
    }
    return render(request, 'app_blog/post.html', context=context)