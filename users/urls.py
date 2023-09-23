from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import SignUPView, AuthenticationView, AccountUpdateView, AccountView, FavoritesView

app_name = 'users'

urlpatterns = [
    path('login', AuthenticationView.as_view(), name='login'),
    path('signup', SignUPView.as_view(), name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('account/<slug:slug>/favorites', FavoritesView.as_view(), name='favorites'),
    path('account/<slug:slug>', AccountView.as_view(), name='account'),
    path('account/<slug:slug>/update', AccountUpdateView.as_view(), name='account_update'),
]
