from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question', 'answer_en', 'question_hi', 'question_bn')
    fieldsets = (
        (_('English Content'), {
            'fields': ('question', 'answer')
        }),
        (_('Hindi Content'), {
            'fields': ('question_hi', 'answer_hi'),
            'classes': ('collapse',)
        }),
        (_('Bengali Content'), {
            'fields': ('question_bn', 'answer_bn'),
            'classes': ('collapse',)
        }),
        (_('Settings'), {
            'fields': ('is_active',)
        })
    )