from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from .models import Profile, Review, Snowboard, Comment

# For customizing the admin site
class MyAdminSite(admin.AdminSite):
    site_header = "Snowboard Reviews administration"
    site_title = "Snowboard Reviews admin"

admin_site = MyAdminSite(name='admin')

# profile admin is used to display the is_reviewer field in the admin site
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_reviewer')

# register the models with the admin site
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

admin_site.register(Profile, ProfileAdmin)

# review admin is used to display the reviewer and snowboard fields in the admin site
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'snowboard')

# register the models with the admin site
admin_site.register(Review, ReviewsAdmin)
admin_site.register(Snowboard)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'user', 'snowboard')

# register the comment model with the admin site
admin_site.register(Comment, CommentAdmin)