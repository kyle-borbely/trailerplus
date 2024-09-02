import requests
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePage, route
from wagtail.admin.edit_handlers import (
    StreamFieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
    BaseChooserPanel,
    FieldPanel,
)

from django.db import models
from django.shortcuts import Http404
from django.db.models import Q, Max, Min
from django.core.exceptions import ObjectDoesNotExist
from django.template.response import TemplateResponse
# Utils
from wagtail.core.url_routing import RouteResult

from wagtail.snippets.models import register_snippet
from trailersplus.settings import TRUSTPILOT_BUSINESS_UNIT, TRUSTPILOT_API_KEY
from trailersplus.utils.decorators import additional_context, define_user_location
from trailersplus.utils.objects import multiple_q
from datetime import date, timedelta
from django.utils.translation import get_language
from collections import Counter, deque
import re
from django.core.cache import cache
# Django Models
from api.models import ServiceReviews
from product.models import Location, CategoryMap, Trailer, Category
# Page Blocks
from streams.splitted_blocks.commerce_blocks import my_store_blocks
from streams.splitted_blocks.commerce_blocks import inventory_blocks
from streams.splitted_blocks.commerce_blocks import category_blocks
from streams.splitted_blocks.commerce_blocks import detail_page_blocks
from streams import blocks as common_blocks
from home.models import Partners, Footer, Header
from menus.models import MainMenu
from .templatetags.product_tags import extend_title

def get_store_trailers(store):
    normal_filters = [Q(store=store), Q(status__in=(100, 120))]
    sold_filters = [Q(store=store), Q(status__exact=150), Q(sale_date__gte=(date.today() - timedelta(days=14)))]
    trailers = Trailer.objects.none()
    for category in CategoryMap.objects.prefetch_related('include', 'exclude').all():
        category_trailers = Trailer.objects.prefetch_related('trailertranslation_set').filter(*normal_filters + [multiple_q(_form_q_filters(category.include.all())) &~ multiple_q(_form_q_filters(category.exclude.all()))])
        if category_trailers:
            trailers |= category_trailers
            trailers |= Trailer.objects.prefetch_related('trailertranslation_set').filter(*sold_filters + [multiple_q(_form_q_filters(category.include.all())) &~ multiple_q(_form_q_filters(category.exclude.all()))])[:12]
    return trailers


# def _get_types_filter(store, url_category, sub_category_url, store_trailers, count=False):
#     result = cache.get(f'{store.pk}_filters_count_{get_language()}', None)
#     counter = 1
#     if result is None:
#         result = []
#         for category in CategoryMap.objects.all():
#             category_index = counter
#             counter += 1
#             sub_category = {}
#             temp_store_trailers = store_trailers.filter(Q(multiple_q(_form_q_filters(category.include.all())) & ~ multiple_q(
#                     _form_q_filters(category.exclude.all()))))
#             try:
#                 temp_store_trailers = sorted(temp_store_trailers, key=lambda x: int(re.search(r'(\d+)', x.category.web_category).group()))
#             except AttributeError:
#                 temp_store_trailers = sorted(temp_store_trailers, key=lambda x: x.category.web_category)
#             for trailer in temp_store_trailers:
#                 if (web_category := trailer.category.web_category) not in sub_category:
#                     sub_category.update(
#                         {
#                             web_category: {
#                                 "count": 1,
#                                 "index": counter,
#                                 "web_category": web_category,
#                                 "slug": trailer.category.slug,
#                                 "verbose": trailer.category.description,
#                             }
#                         }
#                     )
#                     counter += 1
#                 else:
#                     sub_category[web_category]["count"] += 1
#             if get_language() == 'en':
#                 title = category.name_en
#             else:
#                 title = category.name_es
#             result.append([
#                 title, {
#                     "index": category_index,
#                     "slug": category.slug,
#                     "sub": sorted([(key, value) for key, value in sub_category.items()], key=lambda x: x[1]["index"])
#                 },
#               ]
#             )
#         cache.set(f'{store.pk}_filters_count_{get_language()}', result, 3600 / 4)
#     else:
#         counter = result[-1][1]["index"] + 1
#     if count:
#         return result, counter
#     else:
#         return result


def _get_types_filter(store: Location, query: Trailer.objects, count: bool = False):
    result = cache.get(f'{store.pk}_filters_count_{get_language()}', None)
    if result is None:
        if get_language() == 'es':
            result = [
                [
                    'Carga',
                    {
                        'index': 1,
                        'slug': 'Cargo',
                        'sub': [
                            {'Enc4': {
                                'count': query.filter(category__web_category__iexact='Enc4').count(),
                                'index': 1,
                                'web_category': 'Enc4',
                                'slug': '4-Wide-Cargo-Trailers',
                                'verbose': '4\' Carga'
                            }},
                            {'Enc5': {
                                'count': query.filter(category__web_category__iexact='Enc5').count(),
                                'index': 2,
                                'web_category': 'Enc5',
                                'slug': '5-Wide-Cargo-Trailers',
                                'verbose': '5\' Carga'
                            }},
                            {'Enc6': {
                                'count': query.filter(category__web_category__iexact='Enc6').count(),
                                'index': 3,
                                'web_category': 'Enc6',
                                'slug': '6-Wide-Cargo-Trailers',
                                'verbose': '6\' Carga'
                            }},
                            {'Enc6TA': {
                                'count': query.filter(category__web_category__iexact='Enc6TA').count(),
                                'index': 4,
                                'web_category': 'Enc6TA',
                                'slug': '6-Wide-Tandem-Cargo-Trailers',
                                'verbose': '6\' Tandem Carga'
                            }},
                            {'Enc7': {
                                'count': query.filter(category__web_category__iexact='Enc7').count(),
                                'index': 5,
                                'web_category': 'Enc7',
                                'slug': '7-Wide-Cargo-Trailers',
                                'verbose': '7\' Carga'
                            }},
                            {'Enc102': {
                                'count': query.filter(category__web_category__iexact='Enc102').count(),
                                'index': 6,
                                'web_category': 'Enc102',
                                'slug': '8-5-Wide-Cargo-Trailers',
                                'verbose': '8.5\' Carga'
                            }},
                            {'EncCC': {
                                'count': query.filter(category__web_category__iexact='EncCC').count(),
                                'index': 7,
                                'web_category': 'EncCC',
                                'slug': 'Enclosed-Car-Haulers',
                                'verbose': 'Cerrado Porta vehiculos'
                            }},
                        ]
                    }
                ],
                [
                    'Utilitario',
                    {
                        'index': 2,
                        'slug': 'Utility',
                        'sub': [
                            {'Flt4': {
                                'count': query.filter(category__web_category__iexact='Flt4').count(),
                                'index': 8,
                                'web_category': 'Flt4',
                                'slug': '4-Wide-Utility-Trailers',
                                'verbose': '4\' Utilitario'
                            }},
                            {'Flt5': {
                                'count': query.filter(category__web_category__iexact='Flt5').count(),
                                'index': 9,
                                'web_category': 'Flt5',
                                'slug': '5-Wide-Utility-Trailers',
                                'verbose': '5\' Utilitario'
                            }},
                            {'Flt6': {
                                'count': query.filter(category__web_category__iexact='Flt6').count(),
                                'index': 10,
                                'web_category': 'Flt6',
                                'slug': '6-Wide-Utility-Trailers',
                                'verbose': '6\' Utilitario'
                            }},
                            {'Flt6TA': {
                                'count': query.filter(category__web_category__iexact='Flt6TA').count(),
                                'index': 11,
                                'web_category': 'Flt6TA',
                                'slug': '6-Wide-Tandem-Utility-Trailers',
                                'verbose': '6\' Tandem Utilitario'
                            }},
                            {'Flt7': {
                                'count': query.filter(category__web_category__iexact='Flt7').count(),
                                'index': 12,
                                'web_category': 'Flt7',
                                'slug': '7-Wide-Utility-Trailers',
                                'verbose': '7\' Utilitario'
                            }},
                            {'Flt7TA': {
                                'count': query.filter(category__web_category__iexact='Flt7TA').count(),
                                'index': 13,
                                'web_category': 'Flt7TA',
                                'slug': '7-Wide-Tandem-Utility-Trailers',
                                'verbose': '7\' Tandem Utilitario'
                            }},
                            {'Flt8': {
                                'count': query.filter(category__web_category__iexact='Flt8').count(),
                                'index': 14,
                                'web_category': 'Flt8',
                                'slug': '8-5-Wide-Utility-Trailers',
                                'verbose': '8.5\' Utilitario'
                            }},
                        ]
                    }
                ],
                [
                    'Porta vehiculos',
                    {
                        'index': 3,
                        'slug': 'Hauler',
                        'sub': [
                            {'EncCC': {
                                'count': query.filter(category__web_category__iexact='EncCC').count(),
                                'index': 15,
                                'web_category': 'EncCC',
                                'slug': 'Enclosed-Car-Haulers',
                                'verbose': 'Cerrado Porta vehiculos'
                            }},
                            {'FltCC': {
                                'count': query.filter(category__web_category__iexact='FltCC').count(),
                                'index': 16,
                                'web_category': 'FltCC',
                                'slug': 'Flatbed-Car-Haulers',
                                'verbose': 'Plano Porta vehiculos'
                            }},
                        ]
                    }
                ],
                [
                    'Nieve /ATV',
                    {
                        'index': 4,
                        'slug': 'ATV',
                        'sub': [
                            {'EncATV': {
                                'count': query.filter(category__web_category__iexact='EncATV').count(),
                                'index': 17,
                                'web_category': 'EncATV',
                                'slug': 'Enclosed-ATV-Snowmobile-Trailers',
                                'verbose': 'Cerrado ATV'
                            }},
                            {'FltATV': {
                                'count': query.filter(category__web_category__iexact='FltATV').count(),
                                'index': 18,
                                'web_category': 'FltATV',
                                'slug': 'Flatbed-ATV-Snowmobile-Trailers',
                                'verbose': 'Plano ATV'
                            }},
                        ]
                    }
                ],
                [
                    'Volteo',
                    {
                        'index': 5,
                        'slug': 'Dump',
                        'sub': [
                            {'Dump5': {
                                'count': query.filter(category__web_category__iexact='Dump5').count(),
                                'index': 19,
                                'web_category': 'Dump5',
                                'slug': '5-Wide-Dump-Trailers',
                                'verbose': '5\' Volteo'
                            }},
                            {'Dump6': {
                                'count': query.filter(category__web_category__iexact='Dump6').count(),
                                'index': 20,
                                'web_category': 'Dump6',
                                'slug': '6-Wide-Dump-Trailers',
                                'verbose': '6\' Volteo'
                            }},
                            {'Dump7': {
                                'count': query.filter(category__web_category__iexact='Dump7').count(),
                                'index': 21,
                                'web_category': 'Dump7',
                                'slug': '7-Wide-Dump-Trailers',
                                'verbose': '7\' Volteo'
                            }},
                            {'Dump7goss': {
                                'count': query.filter(
                                    Q(category__web_category__iexact='Dump7') & \
                                    Q(coupler__iexact='GN')).count(),
                                'index': 22,
                                'web_category': 'Dump7GN',
                                'slug': '7-Wide-Dump-Trailers',
                                'verbose': 'Cuello de cisne 7\' Volteo'
                            }},
                        ]
                    }
                ],
                [
                    'Equipo',
                    {
                        'index': 6,
                        'slug': 'Equipment',
                        'sub': [
                            {'Eqp6': {
                                'count': query.filter(category__web_category__iexact='Eqp6').count(),
                                'index': 23,
                                'web_category': 'Eqp6',
                                'slug': '6-Wide-Equipment-Trailers',
                                'verbose': '6\' Equipo'
                            }},
                            {'Eqp7': {
                                'count': query.filter(category__web_category__iexact='Eqp7').count(),
                                'index': 24,
                                'web_category': 'Eqp7',
                                'slug': '7-Wide-Equipment-Trailers',
                                'verbose': '7\' Equipo'
                            }},
                            {'Eqp8': {
                                'count': query.filter(category__web_category__iexact='Eqp8').count(),
                                'index': 25,
                                'web_category': 'Eqp8',
                                'slug': '8-5-Wide-Equipment-Trailers',
                                'verbose': '8.5\' Equipo'
                            }},
                        ]
                    }
                ],
                ['Cuello de cisne',{
                    'index': 7,
                    'slug': 'Gooseneck',
                    'sub': [
                        {'Dump7': {
                            'count': query.filter(
                                Q(category__web_category__iexact='Dump7') &\
                                Q(coupler__iexact='GN')).count(),
                            'index': 26,
                            'web_category': 'Dump7GN',
                            'slug': '7-Wide-Dump-Trailers',
                            'verbose': 'Cuello de cisne 7\' Volteo'
                        }},
                        {'Eqp8': {
                            'index': 27,
                            'count': query.filter(
                                Q(category__web_category__iexact='Eqp8') &\
                                Q(coupler__iexact='GN')).count(),
                            'web_category': 'Eqp8GN',
                            'slug': '8-5-Wide-Equipment-Trailers',
                            'verbose': 'Cuello de cisne 8.5\' Equipo'
                        }},
                    ]
                }]
            ]
        else:
            result = [
                [
                    'Cargo',
                    {
                        'index': 1,
                        'slug': 'Cargo',
                        'sub': [
                            {'Enc4': {
                                'count': query.filter(category__web_category__iexact='Enc4').count(),
                                'index': 1,
                                'web_category': 'Enc4',
                                'slug': '4-Wide-Cargo-Trailers',
                                'verbose': '4\' Cargo'
                            }},
                            {'Enc5': {
                                'count': query.filter(category__web_category__iexact='Enc5').count(),
                                'index': 2,
                                'web_category': 'Enc5',
                                'slug': '5-Wide-Cargo-Trailers',
                                'verbose': '5\' Cargo'
                            }},
                            {'Enc6': {
                                'count': query.filter(category__web_category__iexact='Enc6').count(),
                                'index': 3,
                                'web_category': 'Enc6',
                                'slug': '6-Wide-Cargo-Trailers',
                                'verbose': '6\' Cargo'
                            }},
                            {'Enc6TA': {
                                'count': query.filter(category__web_category__iexact='Enc6TA').count(),
                                'index': 4,
                                'web_category': 'Enc6TA',
                                'slug': '6-Wide-Tandem-Cargo-Trailers',
                                'verbose': '6\' Tandem Cargo'
                            }},
                            {'Enc7': {
                                'count': query.filter(category__web_category__iexact='Enc7').count(),
                                'index': 5,
                                'web_category': 'Enc7',
                                'slug': '7-Wide-Cargo-Trailers',
                                'verbose': '7\' Cargo'
                            }},
                            {'Enc102': {
                                'count': query.filter(category__web_category__iexact='Enc102').count(),
                                'index': 6,
                                'web_category': 'Enc102',
                                'slug': '8-5-Wide-Cargo-Trailers',
                                'verbose': '8.5\' Cargo'
                            }},
                            {'EncCC': {
                                'count': query.filter(category__web_category__iexact='EncCC').count(),
                                'index': 7,
                                'web_category': 'EncCC',
                                'slug': 'Enclosed-Car-Haulers',
                                'verbose': 'Enclosed Car Hauler'
                            }},
                        ]
                    }
                ],
                [
                    'Utility',
                    {
                        'index': 2,
                        'slug': 'Utility',
                        'sub': [
                            {'Flt4': {
                                'count': query.filter(category__web_category__iexact='Flt4').count(),
                                'index': 8,
                                'web_category': 'Flt4',
                                'slug': '4-Wide-Utility-Trailers',
                                'verbose': '4\' Utility'
                            }},
                            {'Flt5': {
                                'count': query.filter(category__web_category__iexact='Flt5').count(),
                                'index': 9,
                                'web_category': 'Flt5',
                                'slug': '5-Wide-Utility-Trailers',
                                'verbose': '5\' Utility'
                            }},
                            {'Flt6': {
                                'count': query.filter(category__web_category__iexact='Flt6').count(),
                                'index': 10,
                                'web_category': 'Flt6',
                                'slug': '6-Wide-Utility-Trailers',
                                'verbose': '6\' Utility'
                            }},
                            {'Flt6TA': {
                                'count': query.filter(category__web_category__iexact='Flt6TA').count(),
                                'index': 11,
                                'web_category': 'Flt6TA',
                                'slug': '6-Wide-Tandem-Utility-Trailers',
                                'verbose': '6\' Tandem Utility'
                            }},
                            {'Flt7': {
                                'count': query.filter(category__web_category__iexact='Flt7').count(),
                                'index': 12,
                                'web_category': 'Flt7',
                                'slug': '7-Wide-Utility-Trailers',
                                'verbose': '7\' Utility'
                            }},
                            {'Flt7TA': {
                                'count': query.filter(category__web_category__iexact='Flt7TA').count(),
                                'index': 13,
                                'web_category': 'Flt7TA',
                                'slug': '7-Wide-Tandem-Utility-Trailers',
                                'verbose': '7\' Tandem Utility'
                            }},
                            {'Flt8': {
                                'count': query.filter(category__web_category__iexact='Flt8').count(),
                                'index': 14,
                                'web_category': 'Flt8',
                                'slug': '8-5-Wide-Utility-Trailers',
                                'verbose': '8.5\' Utility'
                            }},
                        ]
                    }
                ],
                [
                    'Car Hauler',
                    {
                        'index': 3,
                        'slug': 'Hauler',
                        'sub': [
                            {'EncCC': {
                                'count': query.filter(category__web_category__iexact='EncCC').count(),
                                'index': 15,
                                'web_category': 'EncCC',
                                'slug': 'Enclosed-Car-Haulers',
                                'verbose': 'Enclosed Car Hauler'
                            }},
                            {'FltCC': {
                                'count': query.filter(category__web_category__iexact='FltCC').count(),
                                'index': 16,
                                'web_category': 'FltCC',
                                'slug': 'Flatbed-Car-Haulers',
                                'verbose': 'Flatbed Car Hauler'
                            }},
                        ]
                    }
                ],
                [
                    'Snow /ATV',
                    {
                        'index': 4,
                        'slug': 'ATV',
                        'sub': [
                            {'EncATV': {
                                'count': query.filter(category__web_category__iexact='EncATV').count(),
                                'index': 17,
                                'web_category': 'EncATV',
                                'slug': 'Enclosed-ATV-Snowmobile-Trailers',
                                'verbose': 'Enclosed ATV'
                            }},
                            {'FltATV': {
                                'count': query.filter(category__web_category__iexact='FltATV').count(),
                                'index': 18,
                                'web_category': 'FltATV',
                                'slug': 'Flatbed-ATV-Snowmobile-Trailers',
                                'verbose': 'Flatbed ATV'
                            }},
                        ]
                    }
                ],
                [
                    'Dump',
                    {
                        'index': 5,
                        'slug': 'Dump',
                        'sub': [
                            {'Dump5': {
                                'count': query.filter(category__web_category__iexact='Dump5').count(),
                                'index': 19,
                                'web_category': 'Dump5',
                                'slug': '5-Wide-Dump-Trailers',
                                'verbose': '5\' Dump'
                            }},
                            {'Dump6': {
                                'count': query.filter(category__web_category__iexact='Dump6').count(),
                                'index': 20,
                                'web_category': 'Dump6',
                                'slug': '6-Wide-Dump-Trailers',
                                'verbose': '6\' Dump'
                            }},
                            {'Dump7': {
                                'count': query.filter(category__web_category__iexact='Dump7').count(),
                                'index': 21,
                                'web_category': 'Dump7',
                                'slug': '7-Wide-Dump-Trailers',
                                'verbose': '7\' Dump'
                            }},
                            {'Dump7': {
                                'count': query.filter(
                                    Q(category__web_category__iexact='Dump7') & \
                                    Q(coupler__iexact='GN')).count(),
                                'index': 22,
                                'web_category': 'Dump7GN',
                                'slug': '7-Wide-Dump-Trailers',
                                'verbose': 'Gooseneck 7\' Dump'
                            }},
                        ]
                    }
                ],
                [
                    'Equipment',
                    {
                        'index': 6,
                        'slug': 'Equipment',
                        'sub': [
                            {'Eqp6': {
                                'count': query.filter(category__web_category__iexact='Eqp6').count(),
                                'index': 23,
                                'web_category': 'Eqp6',
                                'slug': '6-Wide-Equipment-Trailers',
                                'verbose': '6\' Equipment'
                            }},
                            {'Eqp7': {
                                'count': query.filter(category__web_category__iexact='Eqp7').count(),
                                'index': 24,
                                'web_category': 'Eqp7',
                                'slug': '7-Wide-Equipment-Trailers',
                                'verbose': '7\' Equipment'
                            }},
                            {'Eqp8': {
                                'count': query.filter(category__web_category__iexact='Eqp8').count(),
                                'index': 25,
                                'web_category': 'Eqp8',
                                'slug': '8-5-Wide-Equipment-Trailers',
                                'verbose': '8.5\' Equipment'
                            }},
                        ]
                    }
                ],
                ['Gooseneck',{
                    'index': 7,
                    'slug': 'Gooseneck',
                    'sub': [
                        {'Dump7': {
                            'count': query.filter(
                                Q(category__web_category__iexact='Dump7') &\
                                Q(coupler__iexact='GN')).count(),
                            'index': 26,
                            'web_category': 'Dump7GN',
                            'slug': '7-Wide-Dump-Trailers',
                            'verbose': 'Gooseneck 7\' Dump'
                        }},
                        {'Eqp8': {
                            'count': query.filter(
                                Q(category__web_category__iexact='Eqp8') &\
                                Q(coupler__iexact='GN')).count(),
                            'index': 27,
                            'web_category': 'Eqp8GN',
                            'slug': '8-5-Wide-Equipment-Trailers',
                            'verbose': 'Gooseneck 8.5\' Equipment'
                        }},
                    ]
                }]
            ]
        cache.set(f'{store.pk}_filters_count_{get_language()}', result, 3600 / 4)
    if count:
        return result, 26 # ToDo: real map + real count
    else:
        return result


def _form_q_filters(query_set):
    result = []
    for category_filter in query_set:
        pre_template = category_filter.field_name
        if category_filter.case_sensitive:
            template = pre_template + '__'
        else:
            template = pre_template + '__i'
        result.append({f'{template}{category_filter.type}': category_filter.filter})
    return result


@register_snippet
class BannerMessage(models.Model):
    text = models.TextField()

    panels = [FieldPanel('text')]

    class Meta:
        verbose_name = "Banner Message"
        verbose_name_plural = "Banner Messages"


class StatePage(Page):
    def render(self, request, *args, **kwargs):
        raise Http404


class InventoryPage(Page):
    template = "products_base.html"

    content = StreamField(
        [
            ("product_list", inventory_blocks.ProductList()),
            ("additional_message", inventory_blocks.AdditionalMessage()),
            ("social_icons_banner", common_blocks.SocialIconBanner()),
            ("partners", common_blocks.PartnersBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    def _get_trailers_length(self, trailer_query, last_index):
        digit_pattern = re.compile(r"\d+")
        numerical = lambda x: int(digit_pattern.match(x).group())
        counter = Counter(trailer.length for trailer in trailer_query)
        return [(length, {"index": index, "count": count, "numerical": int(digit_pattern.match(length).group())})
                for index, (length, count) in enumerate(sorted(counter.items(), key=lambda x: numerical(x[0])), last_index)]

    @additional_context
    def get_more_context(self, request, store, category, sub_category, *args, **kwargs):
        # Common Context
        context = super(InventoryPage, self).get_context(request, *args, **kwargs)
        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["store"] = store
        # Product List Context
        store_trailers = get_store_trailers(store)
        filters = []
        if category is not None:
            category_map = CategoryMap.objects.prefetch_related('include', 'exclude').get(slug__iexact=category)
            include_filters = multiple_q(_form_q_filters(category_map.include.all()))
            exclude_filters = multiple_q(_form_q_filters(category_map.exclude.all()))
            filters.append(Q(include_filters & ~ exclude_filters))
        elif sub_category is not None:

            filters.append(Q(category__web_category__iexact=sub_category))
        basic_query = store_trailers.select_related('category').filter(*filters)
        context["products"] = dict(
            queryset=[
                {
                    "trailer": trailer,
                    "title": trailer.trailertranslation_set.get(
                        language=get_language().upper()
                    ).tag,
                }
                for trailer in basic_query
            ],
            special=[
                trailer.vin
                for trailer in basic_query
                if (date.today() - trailer.delivery_date).days >= 120
            ],
            count=len(basic_query),
            image_path="/web-pictures/TrailerPictures"
        )
        context["category"] = category
        context["sub_category"] = sub_category
        types, last_index = _get_types_filter(store, store_trailers, True)
        context["filters"] = {
            "lengths": self._get_trailers_length(basic_query, last_index),
            "price": basic_query.aggregate(max=Max('sale_price'), min=Min('sale_price')),
            "types": types,
        }
        context['custom_title'] = f'Trailers Inventory in {store.get_city_name()} - {store.get_state_display()} | TrailersPlus.com'
        context['store_slug'] = store.get_slug()
        return context

    # @define_user_location
    def render(self, request, store, category, sub_category, *args, **kwargs):
        request.is_preview = getattr(request, 'is_preview', False)

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            self.get_more_context(request, store, category, sub_category, *args, **kwargs)
        )


class DetailPage(Page):
    template = "products_base.html"

    content = StreamField(
        [
            ("product_list", detail_page_blocks.ProductPage()),
            ("cta", detail_page_blocks.CTA()),
            ("recently", detail_page_blocks.RecentlyViewed()),
            ("long_info", detail_page_blocks.LongInfo()),
            ("partners", common_blocks.PartnersBlock()),
            ("reserve", detail_page_blocks.Reserve()),
            ("schedule", detail_page_blocks.Schedule()),
            ("appointment", detail_page_blocks.Appointment()),
            ("found_lower", detail_page_blocks.FoundLower()),
            ("additional_message", detail_page_blocks.AdditionalMessage()),
            ("trust_pilot_reviews", common_blocks.TrustPilotWidget()),
            ("trust_pilot_reviews_horizontal", common_blocks.TrustPilotWidgetHorizontal()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    # def get_next_page(self, links):
    #     if len(links):
    #         for link in links:
    #             if link['rel'] == 'next-page':
    #                 return link['href']
    #     raise KeyError('Next page doesn\'t exist')

    # def count_reviews(self, url: str, headers: dict) -> int:
    #     response = requests.get(url, headers=headers).json()
    #     try:
    #         reviews = response['productReviews']
    #     except KeyError:
    #         return 0
    #     try:
    #         next_page = self.get_next_page(response['links'])
    #     except KeyError:
    #         return len(reviews)
    #
    #     return len(reviews) + self.count_reviews(next_page, headers)

    # def get_reviews(self, trailer):
    #     from api.models import TrustpilotCount
    #     all_reviews = trailer.reviews.all().order_by('-created_at')
    #     sku = trailer.category.base_type
    #     try:
    #         count = TrustpilotCount.objects.get(sku=sku).count
    #     except ObjectDoesNotExist:
    #         count = self.count_reviews(
    #             f'https://api.trustpilot.com/v1/product-reviews/business-units/{TRUSTPILOT_BUSINESS_UNIT}/reviews?sku={sku}&perPage=100',
    #             headers={'apikey': TRUSTPILOT_API_KEY}
    #         )
    #         TrustpilotCount.objects.create(sku=sku, count=count)
    #     if len(all_reviews) < 6 and len(all_reviews) != count:
    #         from api.tasks import save_review
    #         data = requests.get(
    #             f'https://api.trustpilot.com/v1/product-reviews/business-units/{TRUSTPILOT_BUSINESS_UNIT}/reviews?&sku={sku}&perPage=6',
    #             headers={'apikey': TRUSTPILOT_API_KEY}
    #         ).json()['productReviews']
    #         for review in data:
    #             review['product'] = {}
    #             review['product']['mnp'] = sku
    #             save_review.delay('product-review-created', review)
    #         all_reviews = trailer.reviews.all().order_by('-created_at')[:6]
    #     return (all_reviews[:6], count) or ([], 0)

    @additional_context
    def get_more_context(self, request, store, category, vin, *args, **kwargs):
        context = super(DetailPage, self).get_context(request, *args, **kwargs)

        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        try:
            trailer = Trailer.objects.select_related('category').prefetch_related('trailertranslation_set', 'reviews').get(vin=vin)
        except ObjectDoesNotExist:
            raise Http404("Trailer Does not Exist")
        trailer_translation = trailer.trailertranslation_set.get(language=get_language().upper())
        recently_deque = deque(request.session.get('recently_viewed', [None] * 4), maxlen=4)
        context["product"] = {
            "common": trailer,
            "trans": trailer_translation
        }
        context["store"] = store
        context["image_path"] = "/web-pictures/Trailers"
        context["reviews"] = {}
        context["reviews"]["data"], context["reviews"]["count"] = trailer.reviews.all().order_by('-created_at')[:6], trailer.reviews.count()
        context["recently"], context["recently"]["trailers"], context["recently"]["special"] = {}, [], []
        deque_remove = []
        for recently_vin in recently_deque:
            if recently_vin is not None:
                try:
                    trailer = Trailer.objects.prefetch_related('trailertranslation_set').get(vin=recently_vin)
                except ObjectDoesNotExist:
                    deque_remove.append(recently_vin)
                else:
                    context["recently"]["trailers"].append(
                        {
                            'trailer': trailer,
                            'title': extend_title(trailer.trailertranslation_set.get(
                                language=get_language().upper()
                            ).short_description, trailer.vin),
                        }
                    )
                    if (date.today() - trailer.delivery_date).days >= 120:
                        context["recently"]["special"].append(trailer.vin)
        for remove_item in deque_remove:
            recently_deque.remove(remove_item)
        context["location"] = {"state": store.state, "full_state": store.get_state_display(), "city": store.store_city}
        if trailer.vin not in recently_deque:
            recently_deque.appendleft(vin)
        request.session['recently_viewed'] = list(recently_deque)
        context['custom_title'] = f'{extend_title(trailer_translation.short_description, trailer.vin)} - {store.store_name} (VIN: {trailer.vin})'
        context['store_slug'] = store.get_slug()
        return context

    # @define_user_location
    def render(self, request, store, category, vin, *args, **kwargs):
        request.is_preview = getattr(request, 'is_preview', False)

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            self.get_more_context(request, store, category, vin, *args, **kwargs)
        )


class CategoryPage(Page):
    template = "category_base.html"

    content = StreamField(
        [
            ("banner", category_blocks.BannerBlock()),
            ("product_list", category_blocks.ProductsBlock()),
            ("bullets", category_blocks.BulletsBlock()),
            ("social_network", common_blocks.SocialIconBanner()),
            ("partners", common_blocks.PartnersBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    @additional_context
    def get_more_context(self, request, store, category, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context['store'] = store
        context['store_slug'] = store.get_slug()
        store_query = get_store_trailers(store)
        context["categories_count"] = _get_types_filter(store, store_query)
        for index, i_category in enumerate(context['categories_count']):
            if i_category[1]['slug'] == 'Gooseneck':
                context['categories_count'].pop(index)
        basic_query = store_query.filter(category__slug__exact=category)
        # basic_query = Trailer.objects.prefetch_related('trailertranslation_set').filter(Q(store=store) & Q(status__in=(100, 120)) & Q(category__slug__exact=category))
        context["products"] = dict(
            queryset=[
                {
                    "trailer": trailer,
                    "title": trailer.trailertranslation_set.get(
                        language=get_language().upper()
                    ).short_description,
                }
                for trailer in basic_query
            ],
            special=[
                trailer.vin
                for trailer in basic_query
                if (date.today() - trailer.delivery_date).days >= 120
            ],
            image_path="/web-pictures/Trailers"
        )
        context['custom_title'] = f'{category.replace("-", " ")} for sale'
        context["category_slug"] = category
        return context

    # @define_user_location
    def render(self, request, store, category, *args, **kwargs):
        request.is_preview = getattr(request, 'is_preview', False)

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            self.get_more_context(request, store, category, *args, **kwargs)
        )


def default_related_store():
    try:
        return Location.objects.first()
    except ObjectDoesNotExist:
        return


class MyStore(RoutablePage):
    template = "store_base.html"

    related_inventory = models.SlugField(
        max_length=50,
        null=False,
        blank=True,
        default='inventory'
    )

    related_category = models.SlugField(
        max_length=50,
        null=False,
        blank=True,
        default='category'
    )

    related_detail = models.SlugField(
        max_length=50,
        null=False,
        blank=True,
        default='detail'
    )

    related_store = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='pages',
        default=default_related_store,
    )

    schema_code = models.TextField(blank=True, null=False, default='')

    content = StreamField(
        [
            ("banner", my_store_blocks.BannerBlock()),
            ("directions", my_store_blocks.DirectionsBlock()),
            ("trust_pilot_reviews", common_blocks.TrustPilotWidget()),
            ("trust_pilot_reviews_horizontal", common_blocks.TrustPilotWidgetHorizontal()),
            ("products", my_store_blocks.ProductsBlock()),
            ("long_text", my_store_blocks.LongTextBlock()),
            ("call_today", my_store_blocks.CallTodayBlock()),
            ("customer_reviews", my_store_blocks.CustomerReviewsBlock()),
            ("one_stop", my_store_blocks.OneStopShopBlock()),
            ("partners", common_blocks.PartnersBlock()),
            ("social", common_blocks.SocialIconBanner()),
            ("get_direction_popup", my_store_blocks.GetDirections()),
            ("appointment_only", detail_page_blocks.Appointment()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel('related_inventory'),
                FieldPanel('related_category'),
                FieldPanel('related_detail'),
            ],
            heading="Related SubPages"
        ),
        BaseChooserPanel('related_store', 'Related Store'),
        FieldPanel('schema_code')
    ]

    def get_slug(self):
        return self.get_url()[1:-1]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super(MyStore, self).get_context(request, *args, **kwargs)
        context["headers"] = Header.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["partners"] = Partners.objects.all()
        context["reviews"] = ServiceReviews.objects.all().order_by("-created_at")[:10]
        context["store"] = self.related_store
        context["stores"] = MyStore.objects.all()
        context["message"] = BannerMessage.objects.last()
        trailers = get_store_trailers(self.related_store)
        count = Counter(trailer.category.slug for trailer in trailers)
        result = []
        for category, num in count.items():
            c_t = trailers.filter(category__slug__iexact=category)
            _trailer_pictures = []
            for trailer in c_t[:5]:
                _trailer_picture = trailer.pictures
                if _trailer_picture is None or not len(_trailer_picture) or _trailer_picture[0] is None:
                    _trailer_pictures.append('comingsoon.jpg')
                else:
                    _trailer_pictures.append(_trailer_picture[0]['file'])

            result.append((category, num, _trailer_pictures, int(c_t.aggregate(Min('sale_price'))['sale_price__min']),
                           c_t[0].category.description))

        context["products"] = sorted(result, key=lambda x: x[3])
        context["products_count"] = len(trailers)
        context["products_image_path"] = "/web-pictures/TrailerPictures"

        en_url_path = ['en'] + self.url_path_en.split('/')[2:]
        es_url_path = ['es'] + self.url_path_es.split('/')[2:]
        context["translation_path"] = {
            "en": '/'.join(en_url_path),
            "es": '/'.join(es_url_path),
        }

        return context

    # @define_user_location
    @route(r'^$')
    def render(self, request, *args, **kwargs):
        request.location = {
            "id": self.related_store.store_id,
            "state": self.related_store.state,
            "full_state": self.related_store.get_state_display(),
            "city": self.related_store.store_city,
            "phone": self.related_store.store_phone,
            "slug": self.related_store.get_slug(),
            "city_name": self.related_store.get_city_name(),
            "map_url": self.related_store.store_map_url,
            "count": int(get_store_trailers(self.related_store).count()),
        }
        return super(MyStore, self).serve(request, *args, **kwargs)

    @route(r'^inventory/$')
    @route(r'^inventory/(\w+)/$')
    @route(r'^inventory/(\w+)/(\w+)/$')
    def render_inv(self, request, category=None, sub_category=None, *args, **kwargs):
        request.location = {
            "id": self.related_store.store_id,
            "state": self.related_store.state,
            "full_state": self.related_store.get_state_display(),
            "city": self.related_store.store_city,
            "phone": self.related_store.store_phone,
            "slug": self.related_store.get_slug(),
            "city_name": self.related_store.get_city_name(),
            "map_url": self.related_store.store_map_url,
            "count": int(get_store_trailers(self.related_store).count()),
        }
        if category is not None:
            if category.lower() in (
                'cargo',
                'utility',
                'hauler',
                'atv',
                'dump',
                'equipment',
                'gooseneck'
            ):
                pass
                # if category.lower() == 'atv':
                #     if not category.isupper():
                #         raise Http404
                #     else:
                #         pass
                # else:
                #     if not category[0].isupper() or\
                #             not category[1:].islower():
                #         raise Http404
                #     else:
                #         pass
            else:
                raise Http404
        if sub_category is not None and\
                sub_category.lower() not in set([cat.web_category.lower() for cat in Category.objects.all()]):
            raise Http404
        elif sub_category is not None:
            if not len(Category.objects.filter(web_category__exact=sub_category)):
                raise Http404
        else:
            pass
        store = self.related_store
        inventory_page = InventoryPage.objects.get(slug_en=self.related_inventory)
        return inventory_page.render(request, store, category, sub_category, *args, **kwargs)

    @route(r'^([0-9a-zA-Z\-]+)/trailer/(\w+)/$')
    def render_detail(self, request, category, vin, *args, **kwargs):
        request.location = {
            "id": self.related_store.store_id,
            "state": self.related_store.state,
            "full_state": self.related_store.get_state_display(),
            "city": self.related_store.store_city,
            "phone": self.related_store.store_phone,
            "slug": self.related_store.get_slug(),
            "city_name": self.related_store.get_city_name(),
            "map_url": self.related_store.store_map_url,
            "count": int(get_store_trailers(self.related_store).count()),
        }
        if category.lower() not in set([cat.slug.lower() for cat in Category.objects.all()]):
            raise Http404
        else:
            if not len(Category.objects.filter(slug__exact=category)):
                raise Http404
        if not vin.isupper():
            raise Http404
        store = self.related_store
        detail_page = DetailPage.objects.get(slug_en=self.related_detail)
        return detail_page.render(request, store, category, vin, *args, **kwargs)

    @route(r'^([0-9a-zA-Z\-]+)/$')
    @route(r'^([0-9a-zA-Z\-]+)//$')
    def render_category(self, request, category, *args, **kwargs):
        request.location = {
            "id": self.related_store.store_id,
            "state": self.related_store.state,
            "full_state": self.related_store.get_state_display(),
            "city": self.related_store.store_city,
            "phone": self.related_store.store_phone,
            "slug": self.related_store.get_slug(),
            "city_name": self.related_store.get_city_name(),
            "map_url": self.related_store.store_map_url,
            "count": int(get_store_trailers(self.related_store).count()),
        }
        if category.lower() not in set([cat.slug.lower() for cat in Category.objects.all()]):
            raise Http404
        else:
            if not len(Category.objects.filter(slug__exact=category)):
                raise Http404
        store = self.related_store
        category_page = CategoryPage.objects.get(slug_en=self.related_category)
        return category_page.render(request, store, category, *args, **kwargs)
