from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('graphfs.urls_api')),
    path('', include('graphfs.urls')),
    path('', RedirectView.as_view(url='/explorer/', permanent=False)),
]
