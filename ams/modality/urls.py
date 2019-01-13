from django.urls import path, include
from rest_framework.routers import DefaultRouter

from modality import views


router = DefaultRouter()
router.register('modalities', views.ModalityViewSet)

app_name = 'modality'

urlpatterns = [
    path('', include(router.urls))
]
