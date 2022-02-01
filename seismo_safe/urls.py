from django.urls import path
from . import views
app_name = 'seismo_safe'

urlpatterns = [
    path('', views.index, name="index")
]