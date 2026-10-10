from django.urls import path
from . import views

urlpatterns = [
    path("", views.ad_list, name="ad_list"),
    path("ads/<int:pk>/", views.ad_detail, name="ad_detail"),
    path("ads/new/", views.ad_create, name="ad_create"),
    path("ads/<int:pk>/edit/", views.ad_update, name="ad_update"),
    path("ads/<int:pk>/delete/", views.ad_delete, name="ad_delete"),
    path("ads/<int:pk>/vote/", views.ad_vote, name="ad_vote"),
    path("ads/<int:pk>/favorite/", views.ad_favorite, name="ad_favorite"),
    path("favorites/", views.favorite_list, name="favorite_list"),
]