from django.apps import AppConfig

class ComplaintsConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'complaints'

    def ready(self):
        import complaints.signals  # Ensure signals are loaded
