from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')), # user
    path('post/', include('post.urls')), # post
    path('reactions/', include('reactions.urls')), # reactions
    path('report/', include('report.urls')), # report
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # avatar
