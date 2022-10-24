from django.contrib import admin
from django.urls import path, include
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
api.add_router('', home_controller)
api.add_router('/categories', categories_controller)
api.add_router('/movies', movies_controller)
api.add_router('/series', series_controller)
api.add_router('/news', news_controller)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
