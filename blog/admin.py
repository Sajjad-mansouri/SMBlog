from django.contrib import admin
from .models import Article,Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','status','published')
    list_filter=('published','status')
    search_fields=('title','description')
    prepopulated_fields={'slug':('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('title','slug','parent','status')
    list_filter=(('status',))
    search_fields=('title','slug')
    prepopulated_fields={'slug':('title',)}