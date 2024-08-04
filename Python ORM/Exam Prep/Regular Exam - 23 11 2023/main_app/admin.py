from django.contrib import admin

from main_app.models import Author, Article, Review


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_banned')
    search_fields = ('full_name', 'email')
    list_filter = ('is_banned',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_on')
    search_fields = ('title',)
    list_filter = ('category',)
    readonly_fields = ('published_on',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'rating', 'published_on')
    search_fields = ('article_reviews__title',)
    list_filter = ('rating','published_on')
    readonly_fields = ('published_on',)