"""Coach URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from user_appointment import views
from django.contrib.auth.views import LoginView

app_name = 'user_appointement'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('connexion/', LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='inscription'),
    path('prendre_rdv/', views.prendre_rdv, name='prendre_rdv'),
    path('', views.home, name='home'),
    path('mes_rdv/', views.mes_rdv, name='mes_rdv'),
    path('rdv_admin/', views.rdv_admin, name='rdv_admin'),
     path('comment/<int:appointment_id>/', views.comment, name='add_comment')
    
]
