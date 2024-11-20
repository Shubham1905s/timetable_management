from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name="myapp"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='myapp:home'), name='logout'),
    path('dashboard/professor/', views.professor_dashboard, name='professor_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
]