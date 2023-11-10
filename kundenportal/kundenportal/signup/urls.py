from django.urls import path
from django.views import generic


appname = 'signup'
urlpatterns = [
    path('', generic.ArchiveIndexView.as_view(), name='signup'),
]
