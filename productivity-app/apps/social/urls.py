from django.urls import path
from . import api

urlpatterns = [
    path('', api.PostListView.as_view(),
         name='feed'),
    path('create', api.CreatePostView.as_view(),
         name="create-post")
]
