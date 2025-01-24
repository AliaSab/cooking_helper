from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Favorite
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import RecipeForm


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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('recipe_list')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/signup.html', {'form': form})


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'recipes/favorite_list.html', {'favorites': favorites})

@login_required
def profile(request):
    user = request.user
    return render(request, 'recipes/profile.html', {'user': user})

@login_required
def add_to_cart(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = recipe.ingredients.split(',')
    cart = request.session.get('cart', {})
    for ingredient in ingredients:
        ingredient = ingredient.strip()
        if ingredient in cart:
            cart[ingredient] += 1
        else:
            cart[ingredient] = 1
    request.session['cart'] = cart
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    return render(request, 'recipes/cart_detail.html', {'cart': cart})

@login_required
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart_detail')


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user  # Устанавливаем текущего пользователя как создателя рецепта
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})