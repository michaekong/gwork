from django.urls import path
from .api import api
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path("home/",index,name="home"),
    path("begin/",first,name="first"),
    path("mainpage",mainpage,name="mainpage"),
    
    path("", api.urls), # Monte tous les endpoints de l'API sous le chemin de cette application
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)