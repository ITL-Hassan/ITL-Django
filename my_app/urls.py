from django.urls import path
from my_app import views
from django.contrib.auth import views as auth_views

app_name = 'my_app'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('update/<int:num>', views.update, name='update'),
    path('delete/<int:num>', views.delete, name='delete'),
    path(
      'accounts/login/',
      auth_views.LoginView.as_view(template_name='accounts/login.html'),
      name='login'
    ),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
]
