from django.urls import path
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'invests'
urlpatterns = [
    # path('', views.home, name='home'),
    path('invest-chart/', views.invest_chart, name='invest-chart'),
    path('invest-chart2/', views.invest_chart2, name='invest-chart2'),
    path('', views.MainView.as_view(), name='all'),
    path('main/', views.InvestView.as_view(), name='invest_list'),
    path('main/create/', views.InvestCreate.as_view(), name='invest_create'),
    path('main/<int:pk>/update/', views.InvestUpdate.as_view(), name='invest_update'),
    path('main/<int:pk>/delete/', views.InvestDelete.as_view(), name='invest_delete'),
    path('lookup/', views.TypeView.as_view(), name='type_list'),
    path('lookup/create/', views.TypeCreate.as_view(), name='type_create'),
    path('lookup/<int:pk>/update/', views.TypeUpdate.as_view(), name='type_update'),
    path('lookup/<int:pk>/delete/', views.TypeDelete.as_view(), name='type_delete'),
]

# Note that make_ and auto_ give us uniqueness within this application
