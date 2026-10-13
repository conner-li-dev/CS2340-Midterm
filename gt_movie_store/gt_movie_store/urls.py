"""
URL configuration for gt_movie_store project.

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
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from cart.admin import cart_engagement_admin_site
from movies.admin import review_engagement_admin_site

urlpatterns = [
    path('', include('home.urls')),
    path('movies/', include('movies.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),

    # admin stuff
    path('admin/engagement/', include((cart_engagement_admin_site.get_urls(), 'cart_engagement_admin'), namespace='cart_engagement_admin')),
    path('admin/reviews-engagement/', include((review_engagement_admin_site.get_urls(), 'reviews_engagement_admin'), namespace='reviews_engagement_admin')),
    path('admin/', include((admin.site.get_urls(), 'admin'), namespace='admin')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

