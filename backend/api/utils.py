from django.db.models import Sum

from recipes.models import IngredientRecipe


def get_shopping_list(user):
    shopping_list = {}
    ingredients = IngredientRecipe.objects.filter(
        recipe__cart_recipes__user=user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(total=Sum('amount'))
    for ingredient in ingredients:
        amount = ingredient['total']
        name = ingredient['ingredient__name']
        measurement_unit = ingredient['ingredient__measurement_unit']
        shopping_list[name] = {
            'measurement_unit': measurement_unit,
            'amount': amount
        }
    return ([f"{item}: {value['amount']}"
             f" {value['measurement_unit']}\n"
             for item, value in shopping_list.items()]
            )
