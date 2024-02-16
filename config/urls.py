"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from azbankgateways.urls import az_bank_gateways_urls
from transaction.views import go_to_gateway_view, callback_gateway_view

admin.autodiscover() 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/',include('accounts.urls')),
    path('',include('book_store.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('try-to-pay/<str:price>/<int:order>/', go_to_gateway_view, name='try_to_pay'),
    path('callback/', callback_gateway_view, name='callback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
