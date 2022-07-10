import imp
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
#admin.site.register(CustomUser)
#admin.site.register(Accounts)

class AccountAdmin(UserAdmin):
    list_display = ('email','username','first_name','last_name','date_of_birth','user_type','gender','date_created','photo')
    search_fields = ('email','username')
    readonly_fields = ('date_created','id')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account,AccountAdmin)