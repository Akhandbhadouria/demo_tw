from django.apps import AppConfig

class TweetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweet'

    def ready(self):
        import tweet.signals
