from django.urls import path, include
from rest_framework.routers import DefaultRouter

from event import views

router = DefaultRouter()
router.register('events', views.EventViewSet)
router.register('competition', views.CompetitionViewSet)

app_name = 'event'

urlpatterns = [
    path('', include(router.urls))
]
