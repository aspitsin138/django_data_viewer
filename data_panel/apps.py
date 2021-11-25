from django.apps import AppConfig


class DataPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_panel'

    def ready(self):
        import data_panel.signals