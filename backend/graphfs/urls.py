from django.urls import path
from . import views

urlpatterns = [
    path('explorer/', views.explorer, name='explorer'),
    path('node/<uuid:node_id>/', views.node_detail, name='node_detail'),
    path('node/<uuid:node_id>/graph/', views.graph_view, name='graph_view'),
    path('search/', views.search_page, name='search'),
]
