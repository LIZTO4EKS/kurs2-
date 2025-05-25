from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('toggle/<int:pk>/', views.note_toggle_done, name='note_toggle_done'),
    path('signup/', views.signup, name='signup'),
]
