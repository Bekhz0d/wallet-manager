from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
# from django.conf.urls import include, re_path


urlpatterns = [
    path('', include('main.urls')),

] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),

    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
)

# if 'rosetta' in settings.INSTALLED_APPS:
#     urlpatterns += [
#         re_path(r'^rosetta/', include('rosetta.urls'))
#     ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
