"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from activities import views
from django.http import JsonResponse
import os

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'activities', views.ActivityViewSet, basename='activity')
router.register(r'leaderboard', views.LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', views.WorkoutViewSet, basename='workout')

# APIベースURLを返すエンドポイント
def api_base_url(request):
    codespace_name = os.environ.get('CODESPACE_NAME', '')
    if codespace_name:
        url = f"https://{codespace_name}-8000.app.github.dev/api/"
    else:
        url = request.build_absolute_uri('/api/')
    return JsonResponse({'api_base_url': url})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', views.api_root, name='api-root'),
    path('api-base-url/', api_base_url, name='api-base-url'),
]
