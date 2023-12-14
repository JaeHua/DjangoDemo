"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app01 import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('',views.homepage),
    path('update_spider/', views.update_spider, name='update_spider'),
    path('run_spider/', views.run_spider, name='run_spider'),
    path('list_spider/', views.list_spider, name='list_spider'),
    path('run_stock/', views.run_stock, name='run_stock'),
    path('visualize_stock_data/', views.visualize_stock_data, name='visualize_stock_data'),
]
