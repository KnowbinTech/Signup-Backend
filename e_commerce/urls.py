"""
URL configuration for e_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path(f'{settings.URL_PREFIX}super-admin/', admin.site.urls),
]

# Application Urls
urlpatterns += [
    path(f'{settings.URL_PREFIX}setup/', include('setup.urls')),
    path(f'{settings.URL_PREFIX}account/', include('users.urls')),

    path(f'{settings.URL_PREFIX}masterdata/', include('masterdata.urls')),
    path(f'{settings.URL_PREFIX}inventory/', include('inventory.urls')),
    path(f'{settings.URL_PREFIX}products/', include('product.urls')),
    path(f'{settings.URL_PREFIX}customer/', include('customer.urls')),
    path(f'{settings.URL_PREFIX}orders/', include('orders.urls')),
    path(f'{settings.URL_PREFIX}transaction/', include('transaction.urls')),
    path(f'{settings.URL_PREFIX}cms/', include('cms.urls')),
    path(f'{settings.URL_PREFIX}home/', include('home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
