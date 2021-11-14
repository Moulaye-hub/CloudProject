from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

urlpatterns = [

    path('api/', include(router.urls)),
    path('', views.home, name='home'),

    path('files/<str:pk>/', views.download_file, name='download_file'),
    path('files/<str:pk>/', views.download_file_cleared, name='download_file_cleared'),

]