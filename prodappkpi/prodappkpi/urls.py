"""prodappkpi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app import views as v
'''
The URL for ALl web resources to access the web request
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.index, name='index'),
    path('index', v.index, name='index'),
    path('JtlUploadAction', v.JtlUploadAction, name='JtlUploadAction'),
    path('pivot_data',v.pivot_data, name='pivot_data'),
    path('KPI/',v.KPI, name='KPI'),
    path('dataView/',v.dataView, name='dataView'),
    path('graphs/', v.graphs, name='graphs'),
    path('historyView/', v.historyView, name='historyView'),

]