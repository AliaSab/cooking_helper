from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('add_to_favorites/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
]