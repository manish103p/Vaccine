from django.urls import path
from . import views,urls
from django.conf import settings



urlpatterns = [
    path('', views.index,name="index"),
    path('register', views.register_user,name="register"),
    path('loggedin',views.loggedin,name='loggedin'),
    path('login',views.login_gen,name='loginTemp'),
    path('provide_access',views.provide_access,name='provide_access')
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)