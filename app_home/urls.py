from django.urls import path

from app_home.views import index_view, contact_view, about_view, user_agreement_view

app_name = 'app_home'

urlpatterns = [
    path("", index_view, name="home"),
    path("contacts/", contact_view, name="contacts"),
    path("about/", about_view, name="about"),
    path("user_agreement/", user_agreement_view, name="user_agreement"),
]
