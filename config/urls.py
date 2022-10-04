from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from ninja import NinjaAPI

from account.authorization import TokenAuthentication
from account.views import account_controller
from movies.controllers.news import news_controller
from movies.controllers.categories import categories_controller
from movies.controllers.general import home_controller
from movies.controllers.movies import movies_controller
from movies.controllers.series import series_controller

api = NinjaAPI()
api.add_router('/account', account_controller)
api.add_router('', home_controller, auth=TokenAuthentication)
api.add_router('/categories', categories_controller, auth=TokenAuthentication)
api.add_router('/movies', movies_controller, auth=TokenAuthentication)
api.add_router('/series', series_controller, auth=TokenAuthentication)
api.add_router('/news', news_controller, auth=TokenAuthentication)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
