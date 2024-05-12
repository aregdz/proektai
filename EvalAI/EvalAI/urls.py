
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.conf.urls.static import static
from EvalAI import settings
from main import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.main, name='main'),
    path('forms/', views.forms, name='forms'),
    path('forms/results/', views.results, name='results'),
    path("contacts/", views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('download_excel/<str:file_name>/', views.download_excel, name='download_excel'),
    path('kak/', views.kak, name='kak'),
]
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

