from django.urls import path, include
from accounts import views


app_name = 'accounts'

urlpatterns = [
	path('sign_up/', views.sign_up, name='sign_up'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('shared_main/', views.shared_main, name='shared_main'),
]