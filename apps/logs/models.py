import secrets
import hashlib

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

    api_key_hash = models.CharField(max_length=64, unique=True, editable=False, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sources')

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='sources', null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-name', 'created')
        unique_together = ('project', 'name')

    def __str__(self):
        return f'{self.project}/{self.name}'
    
    def save(self, *args, **kwargs):
        if self._state.adding and not self.api_key_hash:
            raw_api_key = self.generate_api_key()

            self.api_key_hash = self.hash_api_key(raw_api_key)
            self._raw_api_key = raw_api_key

        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_api_key():
        return secrets.token_hex(16)
    
    @staticmethod
    def hash_api_key(key):
        return hashlib.sha256(key.encode('utf-8')).hexdigest()
    
    def get_raw_api_key(self):
        return getattr(self, '_raw_api_key', None)


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

    meta_data = models.JSONField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Log entry'
        verbose_name_plural = 'Log entries'
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['source', 'timestamp'], name='log_source_timestamp_idx'),
            models.Index(fields=['level'], name='log_level_idx'),
        ]

    def __str__(self):
        return f'{self.timestamp} {self.level} {self.message}'
