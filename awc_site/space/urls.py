from django.urls import path, include
from space import views


app_name = 'space'

urlpatterns = [
    path('', views.space_list, name='space_list'),                              # 개설된 모든 Public 공간 리스트
    path('search_space/', views.search_space_list, name='search_space_list'),   # 검색한 공간 리스트
    path('create_space/', views.create_space, name='create_space'),             # 공간 생성
    path('<space_name>/write_post/', views.write_post, name='write_post'),      # 공간 안에서 글쓰기
    path('<space_name>/', views.show_space, name='show_space'),                 # 공간 메인 페이지
    path('<space_name>/<int:post_id>/', views.post_detail, name='post_detail'), # 공간 내의 게시글
    path('search_name', views.search_name, name='search_name'),
    path('information', views.information, name='information'),
]
