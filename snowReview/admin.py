from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from .models import Profile, Review, Snowboard, Comment

class MyAdminSite(admin.AdminSite):
    site_header = "Snowboard Reviews administration"
    site_title = "Snowboard Reviews admin"

admin_site = MyAdminSite(name='admin')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_reviewer')

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

admin_site.register(Profile, ProfileAdmin)

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'snowboard')

admin_site.register(Review, ReviewsAdmin)

admin_site.register(Snowboard)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'user', 'snowboard')

admin_site.register(Comment, CommentAdmin)