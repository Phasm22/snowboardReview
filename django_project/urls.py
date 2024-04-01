from snowReview.admin import admin_site  # Import your custom admin site
from django.urls import path, include
urlpatterns = [
path('admin/', admin_site.urls),
#connect path to portfolio_app url s
path('', include('snowReview.urls')),
]