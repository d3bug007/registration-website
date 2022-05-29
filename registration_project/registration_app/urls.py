from django.urls import path
from registration_app import views

#TEMPLATE_URL

app_name = 'registration_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/',views.user_login, name="user_login"),
]
