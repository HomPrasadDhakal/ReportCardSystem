from django.urls import path
from drf_yasg import openapi
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from rest_framework import permissions
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view

admin.site.site_header = "Report Card System Admin"
admin.site.site_title = "Report Card System Admin Portal"
admin.site.index_title = "Welcome to Report Card System Admin Portal"


schema_view = get_schema_view(
    openapi.Info(
        title="Report Card System API",
        default_version="v1",
        description="The Report Card System API is a secure," \
        " scalable RESTful interface designed to automate and streamline" \
        " the process of managing student academic performance. It enables educational institutions and developers" \
        " to integrate core functionalities—such as student management," \
        " subject assignment, mark entry, and report card generation—into their existing digital ecosystems.",
        terms_of_service="https://www.homprasaddhakal.com.np",
        contact=openapi.Contact(email="homprasaddhakal@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('documentation/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('accounts.urls')),
    path('', include('accounts.apis.v1.urls')),
    path('', include('students.apis.v1.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        path("__debug__/", include(debug_toolbar.urls)),
    ]