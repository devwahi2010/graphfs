from django.urls import path
from . import views

urlpatterns = [
    path('nodes/', views.api_nodes, name='api_nodes'),
    path('nodes/<uuid:node_id>/', views.api_node, name='api_node'),
    path('nodes/<uuid:node_id>/around/', views.api_around, name='api_around'),
    path('algos/shortest_path', views.api_shortest_path, name='api_shortest_path'),
    path('algos/cycles', views.api_cycles, name='api_cycles'),
    path('tags/', views.api_create_tag, name='api_create_tag'),
    path('tags/attach/', views.api_attach_tag, name='api_attach_tag'),
]
