from django.db import models
from product.models.django import Trailer


class TestInvoice(models.Model):

    invoice_id = models.CharField('Invoice ID', max_length=25, null=True, blank=True)
    trailer = models.ForeignKey(Trailer, on_delete=models.PROTECT, verbose_name='Trailer')
    customer_email = models.EmailField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.pk} Test Invoice"

    class Meta:
        verbose_name = "Test Invoice"
        verbose_name_plural = "Test Invoices"
