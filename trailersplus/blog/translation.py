from .models import BlogListingPage, BlogDetailPage, RightSideBlogBanner
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(RightSideBlogBanner)
class RightSideBlogBannerTR(TranslationOptions):
    fields = (
        "title",
        "sub_title",
        "button_text",
    )


@register(BlogListingPage)
class BlogListingTR(TranslationOptions):
    fields = (
        "custom_title",
        "load_more_button",
        "read_more_button",
        "content",
    )


@register(BlogDetailPage)
class BlogDetailTR(TranslationOptions):
    fields = (
        "post_title",
        "post_short_description",
        "content",
    )
