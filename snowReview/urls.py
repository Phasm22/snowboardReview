from . import views
from .views import snowboard_view
from django.conf import settings
from django.conf.urls.static import static
from snowReview.admin import admin_site 
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
# Auth urls
path('register/', views.register, name='register'),
path('login/', views.login_view, name='login'),
path('home/', views.home_view, name='home_view'),
path('logout/', views.logout_view, name='logout_view'),
path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),


path('password_reset/', views.do_nothing, name='password_reset'),  # Changed this line
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),

# home url
path('', views.home_view, name='index'),

# snowboard urls
path('snowboard/', snowboard_view, name='snowboard'),
path('snowboard-list/', views.SnowboardListView.as_view(), name='snowboard-list'),
path('snowboard/<int:pk>/', views.SnowboardDetailView.as_view(), name='snowboard-detail'),
path('snowboard/delete/<int:snowboard_id>/', views.delete_snowboard, name='delete-snowboard'),

# add a snowboard
path('snowboard/add/', views.createSnowboard, name='snowboard-add'),

# Guide
path('guide/', views.GuideView.as_view(), name='guide'),

# Reviews
path('snowboard/<int:snowboard_id>/review/', views.add_review, name='add-review'),
path('edit-review/<int:review_id>/', views.edit_review, name='edit-review'),
path('delete-review/<int:review_id>/', views.delete_review, name='delete-review'),

# Comments
path('snowboard/<int:snowboard_id>/add_comment/', views.add_comment, name='add-comment'),
path('edit-comment/<int:comment_id>/', views.edit_comment, name='edit-comment'),
path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete-comment'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
