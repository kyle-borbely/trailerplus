import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.utils.html import escape
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
from wagtail.core import hooks
from wagtail.core.rich_text import LinkHandler


class NewWindowExternalLinkHandler(LinkHandler):
    identifier = "external"

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]
        return '<a href="%s" target="_blank" rel="noopener noreferrer">' % escape(href)


@hooks.register("register_rich_text_features")
def register_rich_text_handlers(features):
    features.register_link_type(NewWindowExternalLinkHandler)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    feature_name = "t-center"
    type_ = "CENTERTEXT"
    tag = "div"

    control = {
        "type": type_,
        "label": "Text Center",
        "description": "Center Text",
        "style": {"display": "block", "text-align": "center",},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {type_: {"element": tag, "props": {"class": "t-center"}}}
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    feature_name = "t-left"
    type_ = "TEXTLEFT"
    tag = "p"

    control = {
        "type": type_,
        "label": "Left Text",
        "description": "Left Text",
        "style": {"display": "block", "text-align": "left",},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {type_: {"element": tag, "props": {"class": "t-left"}}}
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    feature_name = "font-white"
    type_ = "FONT-WHITE"
    tag = "h1"

    control = {
        "type": type_,
        "label": "Font White",
        "description": "Text Color - White",
        "style": {"color": "white",},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {type_: {"element": tag, "props": {"class": "c-white"}}}
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    feature_name = "font-underline"
    type_ = "FONT-UNDERLINE"
    tag = "u"

    control = {
        "type": type_,
        "label": "Font Underline",
        "description": "Text Underline",
        "style": {"text-decoration": "underline",},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {type_: {"element": tag, "props": {"class": "t-underline"}}}
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)
