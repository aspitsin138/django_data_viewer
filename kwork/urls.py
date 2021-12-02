"""kwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from data_panel import views as panel_views

login_view = auth_views.LoginView.as_view(
    template_name='sign-in.html',
    redirect_authenticated_user=True
)
logout_view = auth_views.LogoutView.as_view(template_name='sign-out.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('billing/', panel_views.billing, name="billing"),
    path('sign-in/', login_view, name="sign-in"),
    path('sign-up/', panel_views.register, name="sign-up"),
    path('sign-out/', logout_view, name="sign-out"),
    path('api/', include('api.urls')),
    path('', panel_views.ItemListView.as_view(), name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
