from django.urls import path
from . import views,urls
from django.conf import settings



urlpatterns = [
    path('', views.index,name="index"),
    path('register', views.register_user,name="register"),
    path('loggedin/<district_or_center>/<name>/',views.loggedin,name='loggedin'),
    path('login',views.login_gen,name='login_gen'),
    path('logout',views.logout,name='logout'),
    path('provideaccess',views.provideaccess,name='provideaccess')

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)