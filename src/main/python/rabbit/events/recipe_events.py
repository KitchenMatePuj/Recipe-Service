

def build_recipe_event(recipe, event_type: str):
    return {
        "event": event_type,
        "recipe_id": recipe.recipe_id,
        "title": recipe.title,
        "keycloak_user_id": recipe.keycloak_user_id,
        "cooking_time": recipe.cooking_time,
        "rating_avg": recipe.rating_avg,
        "categories": [recipe.category.name] if recipe.category else []
    }

def build_ingredient_event(ingredient, event_type: str):
    return {
        "event": event_type,
        "ingredient_id": ingredient.ingredient_id,
        "recipe_id": ingredient.recipe_id,
        "name": ingredient.name,
        "measurement_unit": ingredient.measurement_unit
    }