from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("new_listing", views.new_listing, name="new_listing"),

    path("watchlist", views.watchlist_page, name="watchlist_page"),
    path("watchlist/<int:id>", views.watchlist_toggle, name="watchlist_toggle"),

    path("endlist", views.endlist, name="endlist"),
    path("endlist_toggle/<int:id>", views.endlist_toggle, name="endlist_toggle"),

    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),

    path("detail/<int:id>", views.detail, name="detail"),
]
