from django.urls import path

from . import views


urlpatterns = [
    path('', views.opportunities_list, name='opportunities_list'),
    path('post/', views.post_opportunity, name='post_opportunity'),
    path('<int:opp_id>/', views.opportunity_detail, name='opportunity_detail'),
    path('<int:opp_id>/apply/', views.apply_opportunity, name='apply_opportunity'),
]
