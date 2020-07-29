from django.urls import path, include
from .views import NoteListCreateAPIView, NoteUpdateDeleteAPIView

urlpatterns = [
    path('', NoteListCreateAPIView),
    path('<int:pk>/', NoteUpdateDeleteAPIView),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]