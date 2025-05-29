from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('toggle/<int:pk>/', views.note_toggle_done, name='note_toggle_done'),
    path('delete/<int:pk>/', views.note_delete, name='note_delete'),
    path('trash/', views.trash, name='trash'),
    path('restore/<int:pk>/', views.restore_note, name='restore_note'),
    path('permanently_delete/<int:pk>/', views.permanently_delete_note, name='permanently_delete_note'),
    path('signup/', views.signup, name='signup'),
    path('edit/<int:pk>/', views.note_edit, name='note_edit'),
]
