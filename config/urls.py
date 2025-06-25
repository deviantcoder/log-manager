from django.contrib import admin
from django.urls import path
from django.views import generic

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', generic.TemplateView.as_view(template_name="_base.html"))
]
