from django.conf.urls import re_path, url

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    re_path('authors/', views.AuthorListView.as_view(), name='authors'),
   re_path('author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
]
