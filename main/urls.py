from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from main.views import IndexView, catalog, cabinet, catalog_detail, user_logout, delivery, user_login, new_order

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<int:pk>/', catalog_detail, name='catalog_detail'),
    path('cabinet/', cabinet, name='cabinet'),
    path('delivery/', delivery, name='delivery'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('order/', new_order, name='order'),
    path('order/<int:cake_id>', new_order, name='order_standart')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
