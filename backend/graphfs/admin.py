from django.contrib import admin
from .models import Node, Edge

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'size', 'path', 'sha256', 'created_at')
    list_filter = ('type',)
    search_fields = ('name', 'path', 'sha256')

@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'src', 'dst', 'edge_type')
    list_filter = ('edge_type',)
    search_fields = ('src__name', 'dst__name')
