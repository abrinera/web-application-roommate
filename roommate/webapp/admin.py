from django.contrib import admin
from .models import User_detail, Post, Favorites

# Register your models here.
admin.site.register(User_detail)
admin.site.register(Post)
admin.site.register(Favorites)
