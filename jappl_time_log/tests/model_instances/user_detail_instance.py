from model_bakery.recipe import Recipe

from jappl_time_log.models.user_detail_model import UserDetail

user_instance: Recipe = Recipe(UserDetail)
