from django.urls import path, include
from space import views


app_name = 'space'

urlpatterns = [
    path('create_space/', views.create_space, name='create_space'),
    # path('<space_name>/', views.PostList.as_view(), name='show_space'),
    path('<space_name>/write_post/', views.write_post, name='write_post'),
    path('<space_name>/', views.show_space, name='show_space'),

]
