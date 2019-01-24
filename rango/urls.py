from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name ='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
     views.show_category, name = 'show_category'),
]

# The sequence will be stored in the parameter category_name_slug and passed to views.show_category()