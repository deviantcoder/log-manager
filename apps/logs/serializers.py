from django.utils import timezone

from rest_framework import serializers, exceptions

from .models import LogEntry


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ('timestamp', 'level', 'message')

    def validate_level(self, value):
        valid_levels = [choice[0] for choice in LogEntry.LOG_LEVELS.choices]
        value = value.upper()

        if value not in valid_levels:
            raise exceptions.AuthenticationFailed(f'Invalid log level. Must be on of {valid_levels}')

        return value

    def create(self, validated_data):
        if 'timestamp' not in validated_data:
            validated_data['timestamp'] = timezone.now()

        source = self.context.get('source')

        validated_data['source'] = source
        validated_data['project'] = source.project

        return super().create(validated_data)
