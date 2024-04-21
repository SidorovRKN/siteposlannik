from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('part/<slug:slug>/', views.ShowPartView.as_view(), name='part'),
    path('category/<slug:cat_slug>/', views.IndexView.as_view(), name='category'),
    path('searchpart/', views.IndexView.as_view(), name='search'),
    # path('api/v1/partslist/', api.PartsAPIView.as_view()),
]