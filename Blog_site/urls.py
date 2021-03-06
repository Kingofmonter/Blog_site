"""Blog_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,re_path
from django.views.static import serve
from Blog_site import settings
from blog import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('login/',views.login),
    path('logout/', views.logout),
    path('register/',views.register),
    path('upload/', views.upload),
    path('index/', views.index),

    path('get_view_code_img/',views.get_view_code_img),
    path('digg/',views.digg),
    re_path('^$', views.index),

    #media配置
    re_path(r"media/(?P<path>.*)$",serve,{"document_root":settings.MEDIA_ROOT}),

    #个人站点
    re_path('^(?P<username>\w+)$',views.home_site),
    re_path('^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)/$',views.home_site),
    re_path('^(?P<username>\w+)/articles/(?P<article_id>\d+)',views.article_detail),

    #评论
    re_path('comment/',views.comment),

    #后台管理
    re_path('cn_backend/$',views.cn_backend),
    re_path('cn_backend/add_article', views.add_article)
]
