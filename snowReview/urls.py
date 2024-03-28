from . import views
from django.conf import settings
from django.conf.urls.static import static
from snowReview.admin import admin_site 
from django.urls import path, include

urlpatterns = [
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('', views.home_view, name='index'),

path('snowboard/', views.SnowboardListView.as_view(), name='snowboard-list'),
path('snowboard/<int:pk>/', views.SnowboardDetailView.as_view(), name='snowboard-detail'),

# add a snowboard
path('snowboard/add/', views.createSnowboard, name='snowboard-add'),
#path('snowboard/<int:pk>/update/', views.updateSnowboard, name='snowboard-update'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
