from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"locations", views.LocationViewSet, basename="locations")

urlpatterns = router.urls
urlpatterns += [
    path(
        "forms/lower_price", views.LowerPriceCreate.as_view(), name="Lower Price Form"
    ),
    path(
        "forms/appointment", views.AppointmentCreate.as_view(), name="Appointment Form"
    ),
    path("forms/custom", views.CustomCreate.as_view(), name="Custom Trailer Form"),
    path("forms/fleet", views.FleetCreate.as_view(), name="Fleet Trailers Form"),
    path("trustpilot/", views.review_create, name="TrustPilot Webhook"),
    path("product_reviews/", views.ProductReviewsList.as_view(), name='Product Reviews'),
    path("count_trailers/", views.TrailersCount.as_view(), name='Trailers Count'),
    path("session_cart/", views.CartSession.as_view(), name="Session Cart"),
    path("user_location/", views.UserLocation.as_view(), name="Session User Location"),
    path("checkout/", views.CheckoutView.as_view(), name="Checkout view")
]
