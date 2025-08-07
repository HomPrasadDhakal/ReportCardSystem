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
        description=(
            "The Report Card System API is a secure, scalable RESTful interface designed to automate "
            "and streamline the management of student academic performance. It enables educational "
            "institutions and developers to seamlessly integrate essential functionalities such as "
            "student management, subject assignment to report card, mark entry, and report card generation into their "
            "existing digital ecosystems.\n\n"
            "This API implements JWT token authentication to ensure secure access and protect sensitive "
            "academic data. It supports full CRUD operations for managing students and subjects, allowing "
            "easy creation, updating, retrieval, and deletion.\n\n"
            "Key features include:\n"
            "- Creating and updating report cards for students\n"
            "- Adding or updating marks per subject within existing report cards\n"
            "- Retrieving report cards for a specific student in a given academic year\n"
            "- Calculating and returning average marks per subject and overall average for the report card\n\n"
            "This system simplifies academic record-keeping, making it efficient, secure, and highly accessible."
        ),
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