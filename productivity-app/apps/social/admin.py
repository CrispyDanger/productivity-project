from django.contrib import admin
from .models import SocialProfile, Post, Comment, Topic

admin.site.register(SocialProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Topic)
