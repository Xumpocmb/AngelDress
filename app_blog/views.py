from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags
from django.utils.text import Truncator

from app_blog.models import Post


def blog_view(request):
    # Получаем все посты, отсортированные по дате создания (новые сначала)
    posts_list = Post.objects.all().order_by('-created_at')

    # Пагинация - 9 постов на страницу (как в каталоге)
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Для совместимости с пагинацией
        'meta_description': "Актуальные новости и статьи о моде, свадьбах и событиях от Angel Dress",
        'title': 'Блог'
    }
    return render(request, 'app_blog/blog.html', context)


def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Очищаем от HTML-тегов и обрезаем текст
    clean_content = strip_tags(post.content)
    truncated_content = Truncator(clean_content).words(20)

    meta_description = f"{post.title}. {truncated_content}"

    context = {
        'post': post,
        'meta_description': meta_description,
        'title': post.title
    }
    return render(request, 'app_blog/post.html', context)
