from django.urls import path, include
from . import views

def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('', views.projects),
    path('sentry-debug/', trigger_error),
    path('project/<str:pk>', views.project),
    path('get_route', views.get_route, name = 'get_route'),
    path('ticket', views.ticketList, name = 'ticket_list'),
    path('', include('virouteapp.urls'))
]