from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    file_url = models.URLField(blank=True, null=True)
    duration = models.FloatField(help_text="Duration in seconds")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    shared_link = models.URLField(blank=True, null=True, unique=True, db_index=True)
    expires_at = models.DateTimeField(blank=True, null=True)
