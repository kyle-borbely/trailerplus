# Environ set up
import environ

env_file = environ.Path(__file__) - 1 + ".env"
root = environ.Path(__file__) - 3
env = environ.Env(DEBUG=(bool, False), SECURE_SSL_REDIRECT=(bool, True))
environ.Env.read_env(env_file=env_file())

ROOT = root
BASE_DIR = root()

#############################
#    DEPLOY AND SECURITY    #
#############################

DEBUG = env("DEBUG")

INTERNAL_IPS = ['127.0.0.1', '157.245.248.171', 'trailersplus.viewdemo.co']

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


WSGI_APPLICATION = "trailersplus.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ROOT_URLCONF = "trailersplus.urls"

FIXTURE_DIRS = [str(BASE_DIR + 'fixtures')]

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT")
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE")
SECURE_REFERRER_POLICY = env("SECURE_REFERRER_POLICY")
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS")
SESSION_COOKIE_HTTPONLY = False
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

#############################
#        COMPONENTS         #
#############################
INSTALLED_APPS = [
    "wagtail_modeltranslation",
    "wagtail_modeltranslation.makemigrations",
    "wagtail_modeltranslation.migrate",
    "streams",
    "home",
    "search",
    "menus",
    "store",
    "flatpage",
    "site_settings",
    "blog",
    "product",
    "checkout",
    "my_store",
    "wagtailcache",
    "storages",
    "wagtail.contrib.modeladmin",
    "wagtailmenus",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.routable_page",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "wagtail_meta_preview",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wagtailuiplus",
    "wagtailmedia",
    "rest_framework",
    "corsheaders",
    "api.apps.ApiConfig",
    "django_celery_results",
    "django_celery_beat",
    "debug_toolbar",
]


MIDDLEWARE = [
    "wagtailcache.cache.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "trailersplus.middleware.UserLocationMiddleware",
    "trailersplus.middleware.RequestSiteName",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "trailersplus.middleware.LocationTagMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "wagtailcache.cache.FetchFromCacheMiddleware",
]


CORS_ORIGIN_ALLOW_ALL = True

#############################
#           DATA            #
#############################

CACHES = {
    "default": env.cache(),
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
DATABASES = {
    "default": env.db(),
    # "products": env.db("PRODUCTS_DB")
}

# DATABASE_ROUTERS = ['trailersplus.routers.DbRouter']

EMAIL_CONFIG = env.email_url("EMAIL_URL")

vars().update(EMAIL_CONFIG)

SITE_NAME = env.str("SITE_NAME")

#############################
# TRANSLATION AND LOCATION  #
#############################

LANGUAGE_CODE = "en-us"

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ("en", _("English")),
    ("es", _("Spanish")),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("en", "es")

LOCALE_PATH = str(root.path("locale"))

GEOIP_PATH = str(root + "trailersplus" + "locations")
GEOIP_KEY = env("GEOIP_KEY")

#############################
# WAGTAIL STREAM FORMS  #
#############################

WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
    ("streamforms/form_block.html", "Default Form Template"),  # default
    ("streamforms/fleet_sales_form.html", "Fleet Sales Template"),
    ("streamforms/custom_trailer_form.html", "Custom Trailer Template"),
)

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################
# STATICFILES AND TEMPLATES #
#############################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(root + "trailersplus" + "templates"),],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailmenus.context_processors.wagtailmenus",
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = ["django.template.context_processors.request"]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_ROOT = str(root + "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    str(root + "trailersplus" + "static"),
]

MEDIA_ROOT = str(root + "media")
MEDIA_URL = "/media/"

DEFAULT_FILE_STORAGE = env("DJANGO_STORGE")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_CSS_HASHING_METHOD = "content"

# WAGTAILIMAGES_JPEG_QUALITY = 100
# WAGTAILIMAGES_WEBP_QUALITY = 100

#############################
#      BOTO3 SETTINGS       #
#############################
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

#############################
#     WAGTAIL SETTINGS      #
#############################
WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    "bmp": "jpeg",
    "webp": "webp",
}

WAGTAIL_SITE_NAME = "trailersplus"

BASE_URL = "http://example.com"

#############################
#   Django Rest Settings    #
#############################

# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffSetPagination',
#     'PAGE_SIZE': 100,
# }

#############################
#      Celery Settings      #
#############################

CELERY_BROKER_URL = env.str("CELERY_CACHE")
CELERY_RESULT_BACKEND = env.str("RESULTS_CACHE")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# CELERY_TASK_ALWAYS_EAGER = True

TRUSTPILOT_API_KEY = env.str('TRUSTPILOT_API_KEY')
TRUSTPILOT_BUSINESS_UNIT = env.str('TRUSTPILOT_BUSINESS_UNIT')

#############################
#      OG-Facebook Settings      #
#############################

META_PREVIEW_FACEBOOK_TITLE_FIELDS = "og_title,seo_title,title"
META_PREVIEW_FACEBOOK_DESCRIPTION_FIELDS = "og_description,search_description"
META_PREVIEW_FACEBOOK_IMAGE_FIELDS = "og_image"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    }

}

REDIS_MESSAGE = env.str("REDIS_MESSAGE")

AUTHORIZE_LOGIN_ID = env.str("AUTHORIZE_LOGIN_ID")
AUTHORIZE_TRANSACTION_KEY = env.str("AUTHORIZE_TRANSACTION_KEY")
