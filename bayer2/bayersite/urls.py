from django.urls import path

from . import views

urlpatterns = [
	path('xray.html', views.xraysubmit, name = 'xray'),
	path('results.html', views.results, name = 'results'),
	path('', views.index.as_view(), name='index'),
	path('index.html', views.index.as_view(), name = 'index'),
]
