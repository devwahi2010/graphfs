from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Node, Edge
from .serializers import NodeSerializer
from .graph_algos import shortest_path_bfs, detect_cycles, k_hop_subgraph

def explorer(request):
    q = request.GET.get('q', '').strip()
    nodes = Node.objects.all().order_by('-updated_at')[:200]
    if q:
        nodes = Node.objects.filter(
            Q(name__icontains=q) | Q(path__icontains=q)
        ).order_by('type', 'name')[:300]
    return render(request, 'explorer.html', {'nodes': nodes, 'q': q})

def node_detail(request, node_id):
    node = get_object_or_404(Node, id=node_id)
    contains = Edge.objects.filter(src=node, edge_type=Edge.EdgeType.CONTAINS).select_related('dst')
    incoming = Edge.objects.filter(dst=node).select_related('src')
    outgoing = Edge.objects.filter(src=node).select_related('dst')
    return render(request, 'node_detail.html', {
        'node': node,
        'contains': contains,
        'incoming': incoming,
        'outgoing': outgoing,
    })

def graph_view(request, node_id):
    node = get_object_or_404(Node, id=node_id)
    return render(request, 'graph_view.html', { 'node': node })

def search_page(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        results = Node.objects.filter(Q(name__icontains=q) | Q(path__icontains=q))[:500]
    return render(request, 'search.html', { 'q': q, 'results': results })

@api_view(['GET'])
def api_nodes(request):
    q = request.GET.get('q', '').strip()
    qs = Node.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(path__icontains=q))
    data = NodeSerializer(qs[:500], many=True).data
    return Response(data)

@api_view(['GET'])
def api_node(request, node_id):
    node = get_object_or_404(Node, id=node_id)
    return Response(NodeSerializer(node).data)

@api_view(['GET'])
def api_around(request, node_id):
    k = int(request.GET.get('k', '2'))
    sub = k_hop_subgraph(str(node_id), k=k)
    return Response(sub)

@api_view(['GET'])
def api_shortest_path(request):
    src = request.GET.get('src')
    dst = request.GET.get('dst')
    if not src or not dst:
        return Response({'detail': 'src and dst are required'}, status=status.HTTP_400_BAD_REQUEST)
    path = shortest_path_bfs(src, dst)
    return Response({'path': path})

@api_view(['GET'])
def api_cycles(request):
    cycles = detect_cycles(limit=50)
    return Response({'cycles': cycles})

@api_view(['POST'])
def api_create_tag(request):
    name = request.data.get('name', '').strip()
    if not name:
        return Response({'detail': 'name is required'}, status=status.HTTP_400_BAD_REQUEST)
    tag = Node.objects.create(name=name, type=Node.NodeType.TAG)
    return Response(NodeSerializer(tag).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def api_attach_tag(request):
    tag_id = request.data.get('tag_id')
    node_id = request.data.get('node_id')
    tag = get_object_or_404(Node, id=tag_id, type=Node.NodeType.TAG)
    node = get_object_or_404(Node, id=node_id)
    Edge.objects.get_or_create(src=tag, dst=node, edge_type=Edge.EdgeType.TAGGED)
    return Response({'detail': 'tag attached'})
