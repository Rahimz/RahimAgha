from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurants'
    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        import restaurants.signals
