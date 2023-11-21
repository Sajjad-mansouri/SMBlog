from django.contrib import admin
from .models import Post,Category,IpAddress,Hit,About,AboutCategory

@admin.register(Post)
class ArticleAdmin(admin.ModelAdmin):
    list_display=('id','title','slug','author','status','published')
    list_filter=('published','status')
    search_fields=('title','description')
    prepopulated_fields={'slug':('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('title','slug','parent','status')
    list_filter=(('status',))
    search_fields=('title','slug')
    prepopulated_fields={'slug':('title',)}

@admin.register(IpAddress)
class IpAdressAdmin(admin.ModelAdmin):
    list_display=('ip',)

@admin.register(Hit)
class IpAdressAdmin(admin.ModelAdmin):
    list_display=('ip',)

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display=['about_category',]

@admin.register(AboutCategory)
class AboutAdmin(admin.ModelAdmin):
    list_display=['title']