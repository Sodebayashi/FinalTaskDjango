from django.urls import path
from . import views

app_name = 'players'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('game/<int:pk>/search/', views.search, name='search'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('game/<int:game_pk>/create/', views.CreateView.as_view(), name='create'),
    path("<int:pk>/delete/", views.PlayerDeleteView.as_view(), name="delete"),
]

