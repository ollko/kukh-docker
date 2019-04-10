
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    # path(
    #     "users/",
    #     include("engl_course.users.urls", namespace="users"),
    # ),
    # path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("auth/", include("myauth.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
