from django.conf.urls import url, re_path, include
from . import views
urlpatterns = [
    re_path('', views.index, name='index'),
    #url(r'^catalog/', include('catalog.urls')),
]