from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessage


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'note', 'message', 'status']
    list_filter = ['status']


admin.site.register(Setting)
admin.site.register(ContactFormMessage, ContactFormAdmin)
