from django.urls import path
from . import views

urlpatterns = [
    path('', views.connections_page, name='connections_page'),
    path('send/<int:alumni_id>/', views.send_connection, name='send_connection'),
    path('accept/<int:connection_id>/', views.accept_connection, name='accept_connection'),
    path('reject/<int:connection_id>/', views.reject_connection, name='reject_connection'),
    path('withdraw/<int:alumni_id>/', views.withdraw_connection, name='withdraw_connection'),
]