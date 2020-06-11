from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessage, UserProfile


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'note', 'message', 'status']
    list_filter = ['status']


class UserFormAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'phone', 'address', 'city',  'image_tag']


admin.site.register(Setting)
admin.site.register(ContactFormMessage, ContactFormAdmin)
admin.site.register(UserProfile, UserFormAdmin)
