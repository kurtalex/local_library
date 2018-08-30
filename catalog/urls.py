from django.conf.urls import url, re_path, include
from . import views
urlpatterns = [
    re_path('', views.index, name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    #url(r'^catalog/', include('catalog.urls')),
]