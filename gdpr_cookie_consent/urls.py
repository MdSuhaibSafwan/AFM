from django.urls import path
from . import views

app_name = "gdpr_cookie_consent"

urlpatterns = [
    path("", views.cookies_management, name="cookies_management"),
    path("modal-dialog/", views.modal_dialog, name="modal_dialog"),
    path("conditional-html/<slug:slug>/", views.conditional_html, name="conditional_html"),
]
