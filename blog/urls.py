from . import views
from django.urls import path

# urlpatterns = [
#     path('', views.HomePage.as_view(), name='home'),
# ]

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
]