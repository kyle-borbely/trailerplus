from django.views import View
from .models import Trailer, Location
from django.shortcuts import get_object_or_404, get_list_or_404, render


class ProductPage(View):
    from_type = None

    def get(self, request, state, city, vin):
        # store = get_object_or_404(Location, state=state, store_city=city)
        # trailer = get_object_or_404(Trailer, vin=vin, store=store)
        return render(request, "product-page.html")
