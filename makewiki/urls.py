from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin Site
    path('admin/', admin.site.urls),

    # Wiki App
    path('', include('wiki.urls')),
    path('accounts/', include('accounts.utls')),
    path('accounts/', include('django.contrib.auth.urls'))

]
