from django.urls import path
from django.views.generic import TemplateView
from .views import ProductPage

urlpatterns = [
    path(
        "<str:state>/<str:city>/inventory/",
        TemplateView.as_view(template_name="utils/product-list.html"),
    ),
    path("<str:state>/<str:city>/<str:vin>/", ProductPage.as_view()),
]
