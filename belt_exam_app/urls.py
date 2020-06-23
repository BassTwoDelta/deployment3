from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register_user', views.register_user),
    path('login_user', views.login_user),
    path('quotes', views.dashboard),
    path('quotes/<num>', views.edit_page),
    path('quotes/<num>/delete', views.delete_quote),
    path('quotes/<num>/add_to_favorites', views.add_to_fave),
    path('quotes/<num>/remove_from_favorites', views.remove_from_fave),
    path('edit_quote/<num>', views.edit_quote),
    path('contribute_quote', views.contribute_quote),
    path('users/<num>', views.user_page),
    path('logout_user', views.logout_user)
]