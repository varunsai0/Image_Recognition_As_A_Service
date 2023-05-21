"""web_tier URL Configuration

"""
from django.urls import path
from web_tier import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.run_app_tier, name = 'run_app_tier')

]

