from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("building/<int:building_id>/", views.building_detail, name="building_detail"),
    path("floor/<int:floor_id>/", views.floor_detail, name="floor_detail"),
    path("room/<int:room_id>/", views.room_detail, name="room_detail"),
    path("room/<int:room_id>/add_member/", views.add_member, name="add_member"),
    path("member/<int:member_id>/edit/", views.edit_member, name="edit_member"),
    path("member/<int:member_id>/delete/", views.delete_member, name="delete_member"),
]
