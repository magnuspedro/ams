from django.urls import path, include
from rest_framework.routers import DefaultRouter

from voucher import views


router = DefaultRouter()
router.register('', views.VoucherViewSet)

app_name = 'voucher'

urlpatterns = [
    path('', include(router.urls))
]
