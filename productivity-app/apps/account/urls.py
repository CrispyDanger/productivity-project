from django.urls import path
from . import api


urlpatterns = [
    path('me/', api.AccountView.as_view(), name='account-view')
]
