from django.urls import path
from task_manager.labels import views


urlpatterns = [
    path('', views.LabelsPage.as_view()),
    path('create/', views.CreateLabel.as_view(),
         name='create_label'),
    path('<int:pk>/update/', views.UpdateLabel.as_view(),
         name='update_label'),
    path('<int:pk>/delete/', views.DeleteLabel.as_view(),
         name='delete_label')
]
