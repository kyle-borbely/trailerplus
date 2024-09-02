from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
from .models import Custom, Fleet, ProductReviews, ServiceReviews
from smtplib import SMTPConnectError, SMTPServerDisconnected
from .utils import titeliser, get_date, get_trailer
from django.db.utils import IntegrityError


@shared_task(bind=True, default_retry_delay=60)
def custom_email(self, obj_id):
    obj = Custom.objects.get(pk=obj_id)
    try:
        send_mail(
            subject="New Web Lead: Custom Trailer",
            message=obj.report(),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['customfleet@trailersplus.com'],
            fail_silently=False,
        )
    except (SMTPConnectError, SMTPServerDisconnected) as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, default_retry_delay=60)
def fleet_email(self, obj_id):
    obj = Fleet.objects.get(pk=obj_id)
    try:
        send_mail(
            subject="New Web Lead: Fleet Trailer",
            message=obj.report(),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['customfleet@trailersplus.com'],
            fail_silently=False,
        )
    except (SMTPConnectError, SMTPServerDisconnected) as exc:
        raise self.retry(exc=exc)


@shared_task()
def save_review(data_type, data):
    if data_type.lower() == "product-review-created":
        try:
            name = data["consumer"]["displayName"]
        except KeyError:
            name = data["consumer"]["name"]
        try:
            p = ProductReviews.objects.create(
                comment_id=data["id"],
                title=titeliser(data["content"]),
                content=data["content"],
                stars=data["stars"],
                created_at=get_date(data["createdAt"]),
                author=name,
                data_raw=data,
            ).products.set(get_trailer(data["product"]["mpn"]))
            return p
        except IntegrityError:
            return 'Product review already exist'
    elif data_type.lower() == "service-review-created":
        try:
            name = data["consumer"]["displayName"]
        except KeyError:
            name = data["consumer"]["name"]
        try:
            s = ServiceReviews.objects.create(
                comment_id=data["id"],
                title=data["title"][:120],
                content=data["text"],
                stars=data["stars"],
                created_at=get_date(data["createdAt"]),
                author=name,
                data_raw=data,
            )
            return s
        except IntegrityError:
            return 'Service review already exist'
    else:
        return
