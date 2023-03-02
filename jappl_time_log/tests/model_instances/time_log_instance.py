from model_bakery.recipe import Recipe

from jappl_time_log.models.time_log_model import TimeLog

time_log_instance: Recipe = Recipe(TimeLog)
