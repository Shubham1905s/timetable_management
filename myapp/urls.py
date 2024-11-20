from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name="myapp"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/professor/', views.professor_dashboard, name='professor_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-timetable/', views.add_timetable, name='add_timetable'),
]