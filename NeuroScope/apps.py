from django.apps import AppConfig

class NeuroscopeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NeuroScope'

    def ready(self):
        import NeuroScope.signals  # Ensures signals are registered

