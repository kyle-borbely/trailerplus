from django.db import models
from product.models import Trailer
from django.contrib.postgres.fields import JSONField


class LowerPrice(models.Model):
    url = models.URLField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=45)
    zip = models.CharField(max_length=5, blank=True, null=True)

    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


class Appointment(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=45)

    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


class Custom(models.Model):
    name = models.CharField(max_length=180)
    email = models.EmailField()
    zip = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def report(self):
        name = f"Name: {self.name}\n"
        email = f"Email: {self.email}\n"
        zip = f"ZIP: {self.zip}\n"
        description = f"Description: {self.description}\n"
        created_at = f'Created At: {self.created_at.strftime("%m/%d/%y %H:%M")}'
        if zip is not None:
            return name + email + zip + description + created_at
        return name + email + description + created_at


class Fleet(models.Model):
    name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=45)
    excepted_fleet = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def report(self):
        name = f"Name: {self.name}\n"
        email = f"Email: {self.email}\n"
        phone = f"Phone: {self.phone}\n"
        excepted_fleet = f"Excepted Fleet Size: {self.excepted_fleet}\n"
        description = f"Description: {self.description}\n"
        created_at = f'Created At: {self.created_at.strftime("%m/%d/%y %H:%M")}'
        if self.excepted_fleet is not None:
            return name + email + phone + excepted_fleet + description + created_at
        return name + email + phone + description + created_at


class ServiceReviews(models.Model):
    comment_id = models.CharField(max_length=26, primary_key=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    stars = models.IntegerField()
    created_at = models.DateTimeField()
    author = models.CharField(max_length=50)
    data_raw = JSONField()

    def __str__(self):
        return f"{self.author} Service Review"

    class Meta:
        ordering = ["-created_at"]


class ProductReviews(models.Model):
    comment_id = models.CharField(max_length=26, primary_key=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    stars = models.IntegerField()
    created_at = models.DateTimeField()
    author = models.CharField(max_length=120)
    products = models.ManyToManyField(Trailer, related_name="reviews")
    data_raw = JSONField()

    def __str__(self):
        return f"{self.author} Review"

    class Meta:
        ordering = ["-created_at"]


class TrustpilotCount(models.Model):
    sku = models.CharField(max_length=255, primary_key=True)
    count = models.IntegerField(default=0)
