from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='home'),
	path('signup/', views.sign_up, name='sign-up'),
	path('signin/', views.sign_in, name='sign-in'),
	path('settings/', views.settings, name='settings'),
	path('logout/', views.log_out, name='log-out'),
]
