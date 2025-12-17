from django.contrib import admin

from user.models import User

# Register your models here.
#admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userId', 'username','email','created_at')

