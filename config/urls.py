from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from ninja import NinjaAPI

from account.views import account_controller
from movies.controllers.news import news_controller

api = NinjaAPI()
api.add_router('/account', account_controller)
api.add_router('/news', news_controller)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
