

def build_recipe_event(recipe, event_type: str):
    return {
        "event": event_type,
        "recipe_id": recipe.recipe_id,
        "title": recipe.title,
        "keycloak_user_id": recipe.keycloak_user_id,
        "cooking_time": recipe.cooking_time,
        "rating_avg": recipe.rating_avg
    }
