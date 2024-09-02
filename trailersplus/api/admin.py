from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from taggit.models import Tag
from wagtail.documents.models import Document
from wagtail.images.models import Image
from wagtailmedia.models import Media

admin.site.register(LowerPrice)
admin.site.register(Appointment)
admin.site.register(Custom)
admin.site.register(Fleet)
admin.site.register(ServiceReviews)
admin.site.register(ProductReviews)
admin.site.register(TrustpilotCount)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Tag)
admin.site.unregister(Document)
admin.site.unregister(Image)
admin.site.unregister(Media)
# Register your models here.
