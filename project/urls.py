from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from project import settings

# Swagger схема
schema_view = get_schema_view(
    openapi.Info(
        title="INSTAGRAM",
        default_version='v1',
        description="API документация для проекта",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('user/', include('user.urls')),
                  path('post/', include('post.urls')),
                  path('reactions/', include('reactions.urls')),
                  path('report/', include('report.urls')),
                  path('message/', include('message.urls')),

                  # Swagger URL
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Redoc версия
                  path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                  # JSON версия схемы
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
