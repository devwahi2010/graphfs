from rest_framework import serializers
from .models import Node, Edge

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name', 'type', 'path', 'size', 'mime_type', 'sha256', 'created_at', 'updated_at']

class EdgeSerializer(serializers.ModelSerializer):
    src = NodeSerializer(read_only=True)
    dst = NodeSerializer(read_only=True)

    class Meta:
        model = Edge
        fields = ['id', 'src', 'dst', 'edge_type']

class EdgeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ['src', 'dst', 'edge_type']
