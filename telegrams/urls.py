#from django.urls import path
#from . import views

#urlpatterns = [
#    path('', views.dashboard, name='dashboard'),
#]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_telegram, name='create_telegram'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
]
