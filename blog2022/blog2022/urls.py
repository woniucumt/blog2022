"""blog2022 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from blog.views import Home_Home_View, Home_Academic_View, Home_Blog_View,Home_Gallery_View, Aboutme_View, \
    Blog_Index_View, Blog_Detail_View, Category_View, Gallery_View, Comment_View

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', Home_Home_View.as_view(), name='Home_Home_View'),
    url(r'^home_academic/', Home_Academic_View.as_view(), name='Home_Academic_View'),
    url(r'^home_blog/', Home_Blog_View.as_view(), name='Home_Blog_View'),
    url(r'^home_gallery/', Home_Gallery_View.as_view(), name='Home_Gallery_View'),
    url(r'^about_me/', Aboutme_View.as_view(), name='Aboutme_View'),

    url(r'^blogindex/', Blog_Index_View.as_view(), name='Blog_Index_View'),  # 博客首页
    url(r'^blogdetail/(?P<blog_id>\d+)$', Blog_Detail_View.as_view(), name='Blog_Detail_View'),
    url(r'^category/(?P<category_id>\d+)$', Category_View.as_view(), name='Category_View'),
    url(r'^gallery/', Gallery_View.as_view(), name='Gallery_View'),  # 画廊首页
    url(r'^comment/', Comment_View.as_view(), name='Comment_View'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
