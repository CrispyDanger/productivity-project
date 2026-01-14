from django.urls import path
from . import api

urlpatterns = [
    path('', api.PostListView.as_view(),
         name='feed'),
    path('create', api.CreatePostView.as_view(),
         name="create-post"),
    path('post/<uuid:pk>/', api.DeletePostView.as_view(), name='delete-post'),
    path('post/<uuid:post_id>/comments/', api.CommentListView.as_view(),
         name='comments'),
    path('post/<uuid:post_id>/create-comment/', api.CreateCommentView.as_view(),
         name='create-comment'),
    path('post/comment/<uuid:pk>/', api.DeleteCommentView.as_view(),
         name='delete-comment'),
    path('post/<uuid:post_id>/toggle-like/', api.LikePostView.as_view(),
         name='toggle-post-like'),
    path('post/<uuid:post_id>/toggle-repost/', api.RepostView.as_view(),
         name='toggle-repost'),
    path('profile/<str:profile_username>/', api.ProfileView.as_view(),
         name='profile')
]
