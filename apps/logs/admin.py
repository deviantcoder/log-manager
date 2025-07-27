from django.contrib import admin

from .models import LogSource, LogEntry


@admin.register(LogSource)
class LogSourceAdmin(admin.ModelAdmin):
    model = LogSource
    list_display = ('name', 'project', 'source_type', 'status')


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    model = LogEntry
    list_display = ('timestamp', 'level', 'project', 'source')
