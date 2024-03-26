from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from .models import Person

class MyAdminSite(admin.AdminSite):
    site_header = "Snowboard Reviews administration"
    site_title = "Snowboard Reviews admin"


admin_site = MyAdminSite(name='admin')
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

admin_site.register(Person.User)