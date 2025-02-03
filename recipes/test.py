# recipes/tests.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Recipe
from django.urls import reverse

class RecipeAppTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Создаем тестовый рецепт
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            description='A test recipe',
            ingredients='ingredient1 5 l, ingredient2 4 kg',
            instructions='Step 1, Step 2',
            created_by=self.user
        )

        # Создаем клиента
        self.client = Client()

    def test_user_registration(self):
        # Проверяем, что пользователь был создан
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)


    def test_user_login_and_logout(self):
        # Вход пользователя
        login_response = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login_response)

        # Проверяем, что пользователь аутентифицирован
        response = self.client.get(reverse('recipe_list'))
        self.assertContains(response, self.user.username)

        # Выход пользователя
        logout_response = self.client.post(reverse('logout'))
        self.assertRedirects(logout_response, reverse('login'))

        # Проверяем, что пользователь больше не аутентифицирован
        response = self.client.get(reverse('recipe_list'))
        self.assertNotContains(response, self.user.username)

    def test_add_recipe(self):
        # Вход пользователя
        self.client.login(username=self.username, password=self.password)

        # Отправляем POST запрос для добавления рецепта
        response = self.client.post(reverse('add_recipe'), {
            'name': 'Another Test Recipe',
            'description': 'Another test description',
            'ingredients': 'ingredient3 5 l, ingredient4 4 kg',
            'instructions': 'Step 3, Step 4',
            'image': ''
        })

        # Проверяем, что рецепт был создан
        self.assertEqual(Recipe.objects.filter(name='Another Test Recipe').count(), 1)

        # Проверяем, что пользователь был перенаправлен на страницу деталей рецепта
        self.assertRedirects(response, reverse('recipe_detail', args=[2]))

    def test_recipe_list(self):
        # Вход пользователя
        self.client.login(username=self.username, password=self.password)

        # Отправляем GET запрос для списка рецептов
        response = self.client.get(reverse('recipe_list'))

        # Проверяем, что рецепт отображается в списке
        self.assertContains(response, self.recipe.name)

    def test_add_to_cart_and_view_cart(self):
        # Вход пользователя
        self.client.login(username=self.username, password=self.password)

        # Добавляем рецепт в корзину
        response = self.client.get(reverse('add_to_cart', args=[self.recipe.pk]))
        self.assertRedirects(response, reverse('cart_detail'))

        # Отправляем GET запрос для отображения корзины
        response = self.client.get(reverse('cart_detail'))

        # Проверяем, что ингредиенты рецепта отображаются в корзине
        for ingredient in self.recipe.ingredients.split(','):
            self.assertContains(response, " ".join(ingredient.split()[:-2]) + " (" + ingredient.split()[-1] + ")")

    def test_clear_cart(self):
        # Вход пользователя
        self.client.login(username=self.username, password=self.password)

        # Добавляем рецепт в корзину
        self.client.get(reverse('add_to_cart', args=[self.recipe.pk]))

        # Очищаем корзину
        response = self.client.get(reverse('clear_cart'))
        self.assertRedirects(response, reverse('cart_detail'))

        # Отправляем GET запрос для отображения корзины
        response = self.client.get(reverse('cart_detail'))

        # Проверяем, что корзина пуста
        self.assertContains(response, "Shopping Cart")
        self.assertNotContains(response, self.recipe.ingredients)