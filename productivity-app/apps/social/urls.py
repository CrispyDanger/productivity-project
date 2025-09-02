from django.urls import path
from . import api

urlpatterns = [
    path('', api.PostListView.as_view(),
         name='feed')
]
