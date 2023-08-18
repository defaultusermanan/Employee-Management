from . import views
from django.urls import path

urlpatterns = [
    path('',views.login,name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login1',views.login1,name='login1'),
    path('reset_password',views.reset_password,name='reset_password'),
    path('feedback_form',views.feedback_form,name='feedback_form'),
    path('edit_dashboard',views.edit_dashboard,name='edit_dashboard'),
    path('learnings',views.learnings,name='learnings'),
    path('test',views.test,name='test'),
    path('intern',views.intern,name='intern'),
    path('client_email',views.client_email,name='client_email'),
    path('client_email1',views.client_email1,name='client_email1'),
    path('manan',views.manan,name='manan'),
    path('details',views.details,name='details')
    #path('dropdown',views.dropdown,name='dropdown'),
]