from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from main.views import IndexView, catalog, cabinet

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', catalog, name='catalog'),
    path('cabinet/', cabinet, name='cabinet')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
