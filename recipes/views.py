from django.shortcuts import render
from collections import defaultdict

from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Favorite
from django.contrib.auth.decorators import login_required

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def add_to_favorites(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if created:
        return redirect('recipe_detail', pk=pk)
    else:
        favorite.delete()
        return redirect('recipe_detail', pk=pk)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'recipes/favorite_list.html', {'favorites': favorites})
# Create your views here.


@login_required
def shopping_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    ingredients = defaultdict(int)
    for favorite in favorites:
        for ingredient in favorite.recipe.ingredients.split(','):
            ingredient = ingredient.strip()
            ingredients[ingredient] += 1
    return render(request, 'recipes/shopping_list.html', {'ingredients': ingredients})