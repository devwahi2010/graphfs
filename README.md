📂 GraphFS — A Graph-Based File System Manager
🚀 Overview
GraphFS is an industry-grade file system manager that represents files and directories as a graph structure instead of a traditional tree.
This allows advanced queries, visualizations, and graph algorithms to be applied directly on the filesystem.
The project demonstrates strong concepts in Data Structures & Algorithms (DSA), System Design, and Full-Stack Development.
✨ Key Features
📁 Graph-Based Modeling – Files, directories, and tags are nodes; relationships are edges (CONTAINS, DUPLICATE, TAGGED).
🔍 Duplicate Detection – Uses SHA-256 hashing to find and link duplicate files.
🧭 Graph Algorithms – BFS shortest path, DFS cycle detection, k-hop subgraphs.
🌐 Interactive Graph Visualization – Explore your filesystem visually using network graphs.
🏷️ Tagging System – Add tags to files and manage collections easily.
⚡ Scalable Backend – Django + PostgreSQL + Dockerized services.
🎨 Professional UI – TailwindCSS + htmx, responsive and user-friendly.
🛠️ Tech Stack
Layer	Technology
Backend	Django, Django REST Framework
Database	PostgreSQL
Deployment	Docker, Gunicorn
Frontend	TailwindCSS, htmx, Cytoscape.js
Algorithms	BFS, DFS, Graph Traversals, Cycle Detection
System	File scanning, SHA-256 hashing
🖥️ Screenshots
<img width="1232" height="788" alt="image" src="https://github.com/user-attachments/assets/abb5ed43-1d37-4826-9cdf-4afaf23ce495" />

📦 Installation & Usage
1. Clone the repo
git clone https://github.com/devwahi2010/graphfs.git
cd graphfs
2. Run with Docker
docker-compose up --build
3. Access the app
Django Admin → http://localhost:8000/admin
GraphFS UI → http://localhost:8000/
📖 Learning Outcomes
Applied graph theory to real-world systems.
Gained hands-on experience with DSA, databases, and system design.
Built and deployed a production-ready full-stack project with modern tools.
Designed the project end-to-end independently as part of my final-year learning journey.
