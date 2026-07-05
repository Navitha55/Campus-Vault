from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('delete-student/<int:pk>/', views.delete_student_view, name='delete_student'),
    path('edit-student/<int:pk>/', views.edit_student_view, name='edit_student_view'),
    path('logout/', views.logout, name='logout'),
]
