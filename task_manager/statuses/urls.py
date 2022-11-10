from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.StatusesPage.as_view()),
    path('create/', views.CreateStatus.as_view()),
    path('<int:pk>/update/', views.UpdateStatus.as_view(),
         name='update_status'),
    path('<int:pk>/delete/', views.DeleteStatus.as_view(),
         name='delete_status')
]
