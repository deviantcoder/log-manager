from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

from apps.projects.models import Project


User = get_user_model()


class LogSource(models.Model):
    class SOURCE_TYPES(models.TextChoices):
        WEB_APP     = ('web_app', 'Web Application')
        API         = ('api', 'API Service')
        DB          = ('db', 'Database')
        SERVER      = ('server', 'Server/Infrastructure')
        MOBILE_APP  = ('mobile_app', 'Mobile Application')
        IOT         = ('iot', 'IoT Device')
        CUSTOM      = ('custom', 'Custom')

    class SOURCE_STATUSES(models.TextChoices):
        ACTIVE   = ('active', 'Active')
        INACTIVE = ('inactive', 'Inactive')
        ARCHIVED = ('archived', 'Archived')


    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)

    source_type = models.CharField(max_length=25, choices=SOURCE_TYPES.choices)
    status = models.CharField(
        max_length=10, choices=SOURCE_STATUSES.choices, default=SOURCE_STATUSES.ACTIVE
    )

    api_key = models.CharField(max_length=32, unique=True, editable=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sources')

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='sources', null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.api_key:
            self.api_key = self.generate_api_key()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.project}/{self.name}'
    
    def generate_api_key(self):
        return str(uuid4()).replace('-', '')


class LogEntry(models.Model):
    class LOG_LEVELS(models.TextChoices):
        TRACE = ('TRACE', 'Trace')
        DEBUG = ('DEBUG', 'Debug')
        INFO  = ('INFO', 'Info')
        WARN  = ('WARN', 'Warning')
        ERROR = ('ERROR', 'Error')
        FATAL = ('FATAL', 'Fatal')

    timestamp = models.DateTimeField(null=True, blank=True)
    level = models.CharField(max_length=10, choices=LOG_LEVELS.choices, default=LOG_LEVELS.INFO)
    message = models.TextField()

    raw_log = models.TextField()

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='logs')
    source = models.ForeignKey(LogSource, on_delete=models.CASCADE, related_name='logs')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['source', 'timestamp'], name='log_source_timestamp_idx'),
            models.Index(fields=['level'], name='log_level_idx'),
        ]

    def __str__(self):
        return f'{self.timestamp} {self.level} {self.message}'
