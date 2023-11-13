from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import MyUser
from .forms import CustomUserCreationForm


UserAdmin.list_display += ('is_author',)
UserAdmin.fieldsets += (_("profile"), {"fields": ("is_author",)}),
UserAdmin.add_fieldsets += (None, {"fields": ("is_author",)}),

admin.site.register(MyUser,UserAdmin)