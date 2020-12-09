from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('logout/', views.admin_logout_view, name='admin-logout'),
]