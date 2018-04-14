from django.urls import path

from .views import serve

urlpatterns = [
    path('<path:name>', serve, name='dbfiles_file'),
]
