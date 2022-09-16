from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("navire", views.NavireView.as_view(), name="navire"),
    path("mareyeur", views.MareyeurView.as_view(), name="mareyeur"),
    path("register", views.register, name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create_navire", views.CreateNavireView.as_view(), name="create_navire"),
    path("create_mareyeur", views.CreateMareyeurView.as_view(), name="create_mareyeur"),
    path("navire/<slug:slug>", views.NavireDetailsView.as_view(), name="navire_detail"),
    path("mareyeur/<slug:slug>", views.MareyeurDetailsView.as_view(), name="mareyeur_detail"),
    path("document/<int:id>", views.DocumentView.as_view(), name="document"),
    path("delete/navire/<slug:slug>", views.delete_navire, name="delete_navire"),
    path("delete/mareyeur/<slug:slug>", views.delete_mareyeur, name="delete_mareyeur"),
]
# handler404 = 'blog.views.Not_found'
