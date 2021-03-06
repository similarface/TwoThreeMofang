"""TwoThreeMofang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import views

urlpatterns = [
    url(r'index/', views.index),
    url(r'add/', views.add,name='add'),
    url(r'list/', views.ajax_list,name='ajax-list'),
    url(r'dict/', views.ajax_dict,name='ajax-dict'),
    url(r'check/', views.check,name='check'),
    url(r'edit_favorites/', views.edit_favorites,name='edit_favorites'),

]
