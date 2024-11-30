"""viroute URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from virouteapp.views import UserLoginView
from virouteapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views






urlpatterns = [
    path('admin/', admin.site.urls),
    #path ('', include('virouteapp.urls')),
    # path('get_route', include('virouteapp.urls')), #whoever delete this is unable to be a human
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('tickets/', views.ticketList, name='tickets'),
    path('get_image/<str:image_name>/', views.get_image_by_name, name='get_image_by_name'),
    path('update_user/<str:user_id>', views.update_user_info, name='update_user_info'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('password_reset/', views.password_reset, name='password_reset'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)