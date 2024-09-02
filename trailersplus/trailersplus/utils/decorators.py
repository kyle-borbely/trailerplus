from functools import wraps
import re
from django.core.cache import cache
from django.utils.translation import get_language
from django.core.exceptions import ObjectDoesNotExist

from product.models.django import Trailer

from .geo import get_closest
from .objects import list_locations, get_my_store

from my_store.templatetags.product_tags import extend_title


def define_user_location(func):
    @wraps(func)
    def wrapper(instance, request, *args, **kwargs):
        try:
            location = request.COOKIES['my_location']
            if not re.match(r'\w{4}\d{2}', location):
                raise ValueError('Wrong Store ID')
            return func(instance, request, *args, **kwargs)
        except (KeyError, ValueError):
            closest = get_closest(request)
            response = func(instance, request, *args, **kwargs)
            response.set_cookie('my_location', closest)
            return response

    return wrapper


def additional_context(func):
    # ToDo: Add to every get_context
    # Define how to set locations
    # Policy update footer
    @wraps(func)
    def wrapper(instance, request, *args, **kwargs):
        language = get_language()
        location_list = cache.get('locations', None)
        location_count = cache.get('location_count', None)
        if location_list is None or location_count is None:
            location_list, location_count = list_locations()
            cache.set('locations', location_list, 3600/4)
            cache.set('location_count', location_count, 3600/4)
        context = func(instance, request, *args, **kwargs)
        try:
            context['custom_title']
        except KeyError:
            context['custom_title'] = False
        context['locations'] = location_list
        context['location_count'] = location_count
        context["locale"] = language
        try:
            context['location'] = get_my_store(request.COOKIES['my_location'])
        except KeyError:
            context['location'] = get_my_store(get_closest(request))
        context['policy'] = request.COOKIES.get('policy', 'decline')
        try:
            cart_pattern = re.compile(r'[0-9A-Za-z]{10,21}')
            cart_trailer = cart_pattern.search(request.session.get('cart_item', '')).group()
            trailer = Trailer.objects.get(vin=cart_trailer)
        except (ObjectDoesNotExist, ValueError, TypeError, AttributeError):
            context['cart_popup_trailer'] = None
            return context
        context['cart_popup_trailer'] = {
                'id': cart_trailer,
                'title': extend_title(trailer.trailertranslation_set.get(language=language.upper()).short_description, cart_trailer),
                'image': '/web-pictures/Trailers/' + trailer.pictures[0]['file'],
                'store': trailer.store,
                'price': trailer.sale_price,
                'link': f'{trailer.store.get_slug()}/{trailer.category.slug}/trailer/{trailer.vin}',
                'trailer': trailer,
            }
        return context
    return wrapper
