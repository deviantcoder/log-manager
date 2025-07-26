from django.contrib import admin

from .models import LogSource, LogEntry


@admin.register(LogSource)
class LogSourceAdmin(admin.ModelAdmin):
    model = LogSource


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    model = LogEntry
