from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ticket import views


router = DefaultRouter()
router.register('', views.TicketViewSet)
router.register('tickets', views.TicketView)


app_name = 'ticket'

urlpatterns = [
    path('', include(router.urls))
]
