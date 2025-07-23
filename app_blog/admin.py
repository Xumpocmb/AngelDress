from django.contrib import admin

from app_blog.forms import PostForm
from app_blog.models import Post, Author, Tag, AuthorSocial, SocialTypes


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class AuthorSocialInline(admin.TabularInline):
    model = AuthorSocial
    extra = 1  # количество пустых форм для добавления новых записей
    fields = ('type', 'link')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [AuthorSocialInline]


@admin.register(SocialTypes)
class SocialTypesAdmin(admin.ModelAdmin):
    list_display = ('get_name_display',)
    verbose_name = 'Тип социальной сети'
    verbose_name_plural = 'Типы социальных сетей'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    filter_horizontal = ('tags',)
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')



