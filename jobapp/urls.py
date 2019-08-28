from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.job_list, name='job_list'),
    path("logout/", views.logout_request, name="logout_request"),
    path('job/new', views.job_new, name='job_new'),
    path('job/<int:pk>/', views.job_detail, name = "job_detail"),
    path('job/<int:pk>/edit/', views.job_edit,name="job_edit"),
    path('job/<int:pk>/delete/', views.job_delete,name="job_delete"),
    path('signup/', views.signup, name='signup'),
    path('login/',views.login_request, name='login_request'),
    path('job/category/<int:pk>/', views.category, name='category')
]   