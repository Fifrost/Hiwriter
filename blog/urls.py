from django.urls import path
from .views import (
    HomeView, PostCreateView, PostDeleteView, PostUpdateView
)
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('HomeView/', HomeView.as_view(), name='home'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('tag/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=''), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('change_password/', views.change_password, name='change_password'),
]
