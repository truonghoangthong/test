from django.contrib import admin
from django.urls import path, include
from virouteapp.views import UserLoginView, get_csrf_token  # Import view lấy CSRF token
from virouteapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('tickets/', views.ticket_list, name='tickets'),
    path('get_image/<str:image_name>/', views.get_image_by_name, name='get_image_by_name'),
    path('update_user/<str:user_id>/', views.update_user_info, name='update_user_info'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/csrf_token/', views.get_csrf_token, name='csrf_token'),  # Route để lấy CSRF token
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
