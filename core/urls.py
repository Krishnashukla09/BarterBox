from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='index'),  # ✅ Homepage
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('browse/', views.browse_users, name='browse_users'),
    path('swap/<int:user_id>/', views.send_swap_request, name='send_swap_request'),
    path('requests/', views.swap_requests_dashboard, name='swap_requests'),
    path('profile/', views.profile_view, name='profile'),
   

]

