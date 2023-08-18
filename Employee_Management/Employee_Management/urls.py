"""
URL configuration for Employee_Management project.

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
from django.contrib import admin
from django.urls import path
from django.urls import include
from employee import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('login_view/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login1/', views.login1, name='login1'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('feedback_form/', views.feedback_form, name='feedback_form'),
    path('edit_dashboard/', views.edit_dashboard, name='edit_dashboard'),
    path('learnings/', views.learnings, name='learnings'),
    path('test/', views.test, name='test'),  # Added trailing slash
    path('intern/',views.intern,name='intern'),
    path('client_email/',views.client_email,name='client_email'),
    path('client_email1/',views.client_email1,name='client_email1'),
    path('manan/',views.manan,name='manan'),
    path('details/',views.details,name='details')
]
