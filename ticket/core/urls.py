from django.urls import path
from .import views

urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    # path("<slug:movie>/<time>",views.ticket_view,name="book"),
    path("<slug:movie>/<date>/<time>",views.TicketView.as_view(),name="book"),
]
