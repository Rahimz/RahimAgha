"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('bookstore/', include('bookstore.urls', namespace='bookstore')),
    path('contacts/', include('contacts.urls', namespace='contacts')),
    path('quizes/', include('quizes.urls', namespace='quizes')),
    path('accounting/', include('accounting.urls', namespace='accounting')),
    path('api/', include('api.urls', namespace='api')),
    path('videos/', include('videos.urls', namespace='videos')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('ai/', include('ai.urls', namespace='ai')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('', include('generals.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
