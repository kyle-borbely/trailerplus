import re

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from streams import blocks
from streams.splitted_blocks.commerce_blocks import detail_page_blocks as d_blocks
from trailersplus.utils.decorators import define_user_location, additional_context
from django.shortcuts import redirect
from trailersplus.celery import app
from product.models.django import Trailer
from django.utils.translation import get_language
from trailersplus.utils.celery import wait_for_result
from .django import TestInvoice


class RedirectNeeded(Exception):
    """raised to be proceed and call redirect"""
    pass


class CheckoutPage(Page):
    template = "checkout_base.html"

    content = StreamField(
        [
            ('checkout', blocks.CheckoutBlock()),
            ('long_text', d_blocks.LongInfo()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        from home.models import Footer, Header
        from menus.models import MainMenu
        # FixMe: Fix this import
        # If import home.models on top the Circular import error raises
        context["headers"] = Header.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        try:
            cart_pattern = re.compile(r'[0-9A-Za-z]{10,21}')
            trailer_id = cart_pattern.search(request.session.get('cart_item', '')).group()
        except (KeyError, ValueError, TypeError, AttributeError):
            try:
                raise RedirectNeeded(request.META['HTTP_REFERER'])
            except KeyError:
                raise RedirectNeeded(f'{request.scheme}://{request.site_name}/')
        trailer = Trailer.objects.get(vin=trailer_id)
        context["cart_trailer"] = {
            'info': trailer,
            'title': trailer.trailertranslation_set.get(language=get_language().upper()).short_description,
            'image_path': '/web-pictures/Trailers',
            'store': trailer.store

        }

        en_url_path = ['en'] + self.url_path_en.split('/')[2:]
        es_url_path = ['es'] + self.url_path_es.split('/')[2:]
        context["translation_path"] = {
            "en": '/'.join(en_url_path),
            "es": '/'.join(es_url_path),
        }

        return context

    # @define_user_location
    def serve(self, request, *args, **kwargs):
        try:
            return super().serve(request, *args, **kwargs)
        except RedirectNeeded as rd:
            return redirect(str(rd))


class CheckoutTnxPage(Page):
    template = "checkout_base.html"

    content = StreamField(
        [
            ('main_content', blocks.CheckoutTnxBlock()),
            ("social_icons_banner", blocks.SocialIconBanner()),
            ('partners', blocks.PartnersBlock()),

        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        from home.models import Footer, Header, Partners
        from menus.models import MainMenu
        # FixMe: Fix this import
        # If import home.models on top the Circular import error raises
        context["headers"] = Header.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["partners"] = Partners.objects.all()
        invoice_id = str(request.session.get('last_invoice', None))
        print(f"Sucess: {invoice_id=}")
        if invoice_id is None:
            try:
                raise RedirectNeeded(request.META['HTTP_REFERER'])
            except KeyError:
                raise RedirectNeeded(f'{request.scheme}://{request.site_name}/')
        invoice = TestInvoice.objects.get(invoice_id=invoice_id)
        trailer = invoice.trailer
        context["cart_trailer"] = {
            'info': trailer,
            'title': trailer.trailertranslation_set.get(language=get_language().upper()).short_description,
            'image_path': '/web-pictures/Trailers',
            'store': trailer.store
        }
        context["invoice"] = invoice

        en_url_path = ['en'] + self.url_path_en.split('/')[2:]
        es_url_path = ['es'] + self.url_path_es.split('/')[2:]
        context["translation_path"] = {
            "en": '/'.join(en_url_path),
            "es": '/'.join(es_url_path),
        }

        return context

    # @define_user_location
    def serve(self, request, *args, **kwargs):
        try:
            return super().serve(request, *args, **kwargs)
        except RedirectNeeded as rd:
            return redirect(str(rd))
