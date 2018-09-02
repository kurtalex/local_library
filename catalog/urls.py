from django.conf.urls import re_path

from . import views

urlpatterns = [
    re_path('', views.index, name='index'),
    re_path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]
