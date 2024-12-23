from django.apps import AppConfig


class JoinAuthPermissionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'join_auth_permission'
    def ready(self):
        import join_auth_permission.api.signals 
