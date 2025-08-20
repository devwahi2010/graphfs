import os
import mimetypes
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from graphfs.models import Node, Edge
from graphfs.utils.filehash import sha256_file

class Command(BaseCommand):
    help = "Index a filesystem path into GraphFS"

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, required=True, help='Absolute path to index')
        parser.add_argument('--follow-symlinks', action='store_true', help='Follow symlinks when walking')

    def handle(self, *args, **options):
        root_path = options['path']
        follow = options['follow_symlinks']
        p = Path(root_path)
        if not p.exists():
            raise CommandError(f"Path does not exist: {root_path}")

        self.stdout.write(self.style.SUCCESS(f"Indexing: {root_path} (follow_symlinks={follow})"))
        node_cache = {}

        root_node, _ = Node.objects.get_or_create(
            path=str(p.resolve()),
            defaults={
                'name': p.name or str(p.resolve()),
                'type': Node.NodeType.DIR,
                'size': 0,
            }
        )
        node_cache[str(p.resolve())] = root_node

        for dirpath, dirnames, filenames in os.walk(root_path, followlinks=follow):
            dir_abs = str(Path(dirpath).resolve())
            if dir_abs in node_cache:
                dir_node = node_cache[dir_abs]
            else:
                dir_node, _ = Node.objects.get_or_create(
                    path=dir_abs,
                    defaults={'name': Path(dir_abs).name, 'type': Node.NodeType.DIR, 'size': 0}
                )
                node_cache[dir_abs] = dir_node

            for d in dirnames:
                subdir_abs = str(Path(dirpath, d).resolve())
                sub_node, _ = Node.objects.get_or_create(
                    path=subdir_abs,
                    defaults={'name': d, 'type': Node.NodeType.DIR, 'size': 0}
                )
                node_cache[subdir_abs] = sub_node
                Edge.objects.get_or_create(src=dir_node, dst=sub_node, edge_type=Edge.EdgeType.CONTAINS)

            for f in filenames:
                f_abs = str(Path(dirpath, f).resolve())
                try:
                    size = os.path.getsize(f_abs)
                except FileNotFoundError:
                    continue

                mime, _ = mimetypes.guess_type(f_abs)
                file_hash = ""
                try:
                    file_hash = sha256_file(f_abs)
                except Exception:
                    pass

                file_node, created = Node.objects.get_or_create(
                    path=f_abs,
                    defaults={
                        'name': f, 'type': Node.NodeType.FILE, 'size': size,
                        'mime_type': mime or 'application/octet-stream', 'sha256': file_hash
                    }
                )
                if not created:
                    # update metadata if changed
                    updated = False
                    if file_node.size != size:
                        file_node.size = size; updated = True
                    if (file_node.mime_type or '') != (mime or 'application/octet-stream'):
                        file_node.mime_type = mime or 'application/octet-stream'; updated = True
                    if not file_node.sha256 and file_hash:
                        file_node.sha256 = file_hash; updated = True
                    if updated:
                        file_node.save()

                node_cache[f_abs] = file_node
                Edge.objects.get_or_create(src=dir_node, dst=file_node, edge_type=Edge.EdgeType.CONTAINS)

        dup_groups = {}
        for n in Node.objects.filter(type=Node.NodeType.FILE).exclude(sha256__isnull=True).exclude(sha256=""):
            dup_groups.setdefault(n.sha256, []).append(n)

        count_dup_edges = 0
        for h, nodes in dup_groups.items():
            if len(nodes) <= 1: continue
            for i in range(len(nodes)):
                for j in range(i+1, len(nodes)):
                    Edge.objects.get_or_create(src=nodes[i], dst=nodes[j], edge_type=Edge.EdgeType.DUPLICATE)
                    Edge.objects.get_or_create(src=nodes[j], dst=nodes[i], edge_type=Edge.EdgeType.DUPLICATE)
                    count_dup_edges += 2

        self.stdout.write(self.style.SUCCESS(f"Index complete. Duplicate edges created: {count_dup_edges}"))
