import uuid
from django.db import models

class Node(models.Model):
    class NodeType(models.TextChoices):
        FILE = "FILE", "File"
        DIR = "DIR", "Directory"
        TAG = "TAG", "Tag"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512)
    type = models.CharField(max_length=8, choices=NodeType.choices)
    path = models.TextField(blank=True, null=True)  # filesystem path if applicable
    size = models.BigIntegerField(default=0)
    mime_type = models.CharField(max_length=128, blank=True, null=True)
    sha256 = models.CharField(max_length=64, blank=True, null=True, db_index=True)  # file hash for duplicates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.type})"

class Edge(models.Model):
    class EdgeType(models.TextChoices):
        CONTAINS = "CONTAINS", "Contains"   # DIR -> (DIR|FILE)
        SYMLINK = "SYMLINK", "Symlink"     # Node -> Node
        TAGGED = "TAGGED", "Tagged"        # TAG -> Node
        DUPLICATE = "DUPLICATE", "Duplicate" # FILE <-> FILE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    src = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='out_edges')
    dst = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='in_edges')
    edge_type = models.CharField(max_length=16, choices=EdgeType.choices)

    class Meta:
        unique_together = ('src', 'dst', 'edge_type')
        indexes = [
            models.Index(fields=['edge_type']),
        ]

    def __str__(self):
        return f"{self.src} -[{self.edge_type}]-> {self.dst}"
