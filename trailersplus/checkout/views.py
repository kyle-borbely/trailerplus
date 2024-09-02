from decimal import Decimal

import ujson

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt

from trailersplus.celery import app
from trailersplus.utils.celery import wait_for_result
from product.models.django import Trailer
from .forms import InvoiceForm
from .models.django import TestInvoice
from datetime import datetime
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.http import HttpResponse, Http404

from .services import WebsiteApiClient
from authorizenet import apicontractsv1
from authorizenet.constants import constants
from authorizenet.apicontrollers import createTransactionController
from django.conf import settings

from uuid import uuid4


# def submit(request):
#     customer_data = dict(
#         first_name=request.POST['firstname'],
#         last_name=request.POST['lastname'],
#         company=request.POST['company'],
#         phone=request.POST['phone'],
#         email=request.POST['email'],
#         trailer=request.POST['trailer_id']
#     )
#     payment_info = dict(
#         billing_address=request.POST['address'],
#         city=request.POST['city'],
#         state=request.POST['state'],
#         zip=request.POST['zip'],
#         cardnumber=request.POST['cardnumber'],
#         ccv=request.POST['ccv'],
#         expirity=request.POST['expirity'],
#     )
#     invoice = wait_for_result(app.send_task('get_invoice', kwargs=customer_data, queue="checkout"))
#     invoice = invoice.result
#     invoice['trailer'] = Trailer.objects.get(vin=invoice['trailer'])
#     invoice['date'] = datetime.strptime(invoice['date'], "%m/%d/%Y")
#     TestInvoice.objects.create(**invoice)
#     request.session['last_invoice'] = invoice['id']
#     del request.session['cart_item']
#     request.session.modified = True
#     return redirect('/success-checkout/')


def prer_submit(request):
    try:
        redis_client = WebsiteApiClient()
        trailer = Trailer.objects.select_related('store').prefetch_related('trailertranslation_set').get(
            vin=request.POST['trailer_id'])
        trailer_verbose = trailer.trailertranslation_set.get(language=get_language().upper())
        full_lang = "English" if get_language().upper() == 'EN' else 'Spanish'
        customer_id = redis_client.get_or_create_customer(
            invoice_name=request.POST["company"] if request.POST["company"] else request.POST['firstname'] + '_' +
                                                                                 request.POST['lastname'],
            first_name=request.POST['firstname'],
            last_name=request.POST['lastname'],
            title=trailer_verbose.short_description,
            email_address=request.POST['email'],
            phone_number=request.POST['phone'],
            address_1=request.POST['address'],
            address_2=request.POST['address'],
            city=request.POST['city'],
            state_short=request.POST['state'],
            postal_code=request.POST['zip'],
            country='USA',
            language=full_lang,
        )
        try:
            customer_id = customer_id['customer_id']
        except KeyError:
            customer_id = uuid4()
        trailer_status = redis_client.trailer_status(request.POST['trailer_id'])
        try:
            trailer_status = trailer_status['status']
        except KeyError:
            trailer_status = 100
        customer_active_reserver = redis_client.customer_active_reserves(customer_id)
        try:
            customer_active_reserver = customer_active_reserver['active_reserves']
        except KeyError:
            customer_active_reserver = 0
        if trailer_status != 100 or customer_active_reserver:
            return redirect('/')
        store_id = trailer.store.store_id
        new_invoice = redis_client.create_invoice(customer_id, store_id, trailer.vin)
        try:
            if new_invoice['error']:
                return redirect('/')
            invoice_number = new_invoice['invoice_number']
        except KeyError:
            invoice_number = uuid4()

        # FAKE TRANSACTION BLOCK

        redis_client.add_reserve_to_invoice()

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZE_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZE_TRANSACTION_KEY

        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = request.POST['cardnumber']
        expirity = request.POST['expirity'].split('/')
        creditCard.expirationDate = f"20{expirity[1]}-{expirity[0]}"
        creditCard.cardCode = request.POST['ccv']

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        order = apicontractsv1.orderType()
        order.invoiceNumber = invoice_number
        order.description = trailer_verbose.short_description

        customerAddress = apicontractsv1.customerAddressType()
        customerAddress.firstName = request.POST['firstname']
        customerAddress.lastName = request.POST['lastname']
        customerAddress.company = request.POST['company']
        customerAddress.address = request.POST['address']
        customerAddress.city = request.POST['city']
        customerAddress.state = request.POST['state']
        customerAddress.zip = request.POST['zip']
        customerAddress.country = "USA"

        customerData = apicontractsv1.customerDataType()
        customerData.type = "company" if request.POST['company'] else "individual"
        customerData.id = customer_id
        customerData.email = request.POST['email']

        duplicateWindowSetting = apicontractsv1.settingType()
        duplicateWindowSetting.settingName = "duplicateWindow"
        duplicateWindowSetting.settingValue = "600"
        settings = apicontractsv1.ArrayOfSetting()
        settings.setting.append(duplicateWindowSetting)

        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authOnlyTransaction"
        transactionrequest.amount = 50
        transactionrequest.payment = payment
        transactionrequest.order = order
        transactionrequest.billTo = customerAddress
        transactionrequest.customer = customerData
        transactionrequest.transactionSettings = settings

        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId = "TrailersPlus"
        createtransactionrequest.transactionRequest = transactionrequest

        createtransactioncontroller = createTransactionController(
            createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()

        if response is not None:
            _res = redis_client.add_reserve_to_invoice(store_id,
                                                       invoice_number,
                                                       response.messages.resultCode,

                                                       response.transactionResponse.transId,
                                                       response.mesages.message)
            try:
                if not _res['error']:
                    return HttpResponse(b"SUCCESS", status=200)
            except KeyError:
                return HttpResponse(b"SUCCESS", status=200)
        return HttpResponse(b"Authorize payment failed", status=400)
    except RuntimeError:
        return HttpResponse(b"Failed, Redis connection timeout", status=400)
    except Exception as e:
        error = {
            "status": 400,
            "error": True,
            "error_text": str(e)
        }
        return HttpResponse(ujson.dumps(error), status=400)


def lxml_to_dict(response):
    result = {k: lxml_to_dict(v) for k, v in response.__dict__.items()}
    if not len(result):
        return str(response)
    else:
        return result


def submit(request):
    trailer = Trailer.objects.select_related('store').prefetch_related('trailertranslation_set').get(
        vin=request.POST['trailer_id'])
    trailer_verbose = trailer.trailertranslation_set.get(language=get_language().upper())
    invoice_number = str(uuid4())[:10]
    customer_id = str(uuid4())[:10]
    try:
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZE_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZE_TRANSACTION_KEY

        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = request.POST['cardnumber'].replace('-', '')
        expirity = request.POST['expirity'].split('/')
        creditCard.expirationDate = f"20{expirity[1]}-{expirity[0]}"
        creditCard.cardCode = request.POST['ccv']

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        order = apicontractsv1.orderType()
        order.invoiceNumber = invoice_number  ###)[:10]
        order.description = trailer_verbose.short_description

        customerAddress = apicontractsv1.customerAddressType()
        customerAddress.firstName = request.POST['firstname']
        customerAddress.lastName = request.POST['lastname']
        customerAddress.company = request.POST['company']
        customerAddress.address = request.POST['address']
        customerAddress.city = request.POST['city']
        customerAddress.state = request.POST['state']
        customerAddress.zip = request.POST['zip']
        customerAddress.country = "USA"

        customerData = apicontractsv1.customerDataType()
        customerData.type = "business" if request.POST['company'] else "individual"
        customerData.id = customer_id  ###
        customerData.email = request.POST['email']

        duplicateWindowSetting = apicontractsv1.settingType()
        duplicateWindowSetting.settingName = "duplicateWindow"
        duplicateWindowSetting.settingValue = "600"
        settings_array = apicontractsv1.ArrayOfSetting()
        settings_array.setting.append(duplicateWindowSetting)

        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authOnlyTransaction"
        transactionrequest.amount = 50
        transactionrequest.payment = payment
        transactionrequest.order = order
        transactionrequest.billTo = customerAddress
        transactionrequest.customer = customerData
        transactionrequest.transactionSettings = settings_array

        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId = "TrailersPlus"
        createtransactionrequest.transactionRequest = transactionrequest

        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()
        if response is not None:
            return HttpResponse(ujson.dumps({
                "authorize": lxml_to_dict(response),
                "data": dict(request.POST)
            }))
        else:
            return HttpResponse(b"Can't get response from Authorize.net")
    except Exception as e:
        return HttpResponse(ujson.dumps({"error": repr(e)}))


class InvoiceView(FormView):
    template_name = "invoice_template.html"
    form_class = InvoiceForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InvoiceView, self).dispatch(request, *args, **kwargs)

    def get(self, request, invoice_id, *args, **kwargs):
        form_class = self.get_form_class()
        form: InvoiceForm = self.get_form(form_class)
        context = self.get_context_data(form=form, invoice_id=invoice_id)
        return self.render_to_response(context)

    def post(self, request, invoice_id, *args, **kwargs):
        form_class = self.get_form_class()
        form: InvoiceForm = self.get_form(form_class)
        context = self.get_context_data(form=form, invoice_id=invoice_id)
        invoice_data = context['invoice']
        if form.is_valid():
            print('Form is valid')
            client = WebsiteApiClient()
            context.update(
                {"additional": {"success": False, "invalid_form": False}}
            )
            try:
                merchantAuth = apicontractsv1.merchantAuthenticationType()
                merchantAuth.name = settings.AUTHORIZE_LOGIN_ID
                merchantAuth.transactionKey = settings.AUTHORIZE_TRANSACTION_KEY

                creditCard = apicontractsv1.creditCardType()
                creditCard.cardNumber = form.cleaned_data['card_num']
                expirity = form.cleaned_data['card_exp'].split('/')
                creditCard.expirationDate = f"20{expirity[1]}-{expirity[0]}"
                creditCard.cardCode = form.cleaned_data['card_code']

                payment = apicontractsv1.paymentType()
                payment.creditCard = creditCard

                order = apicontractsv1.orderType()
                order.invoiceNumber = f"{invoice_data['StoreID']}-{invoice_data['InvoiceNumber']}"  ###)[:10]
                order.description = f"{invoice_data['CustomerName']} {invoice_data['StoreID']}-{invoice_data['InvoiceNumber']} invoice"

                customerAddress = apicontractsv1.customerAddressType()
                customerAddress.firstName = invoice_data['customer_data'][0]['first_name']
                customerAddress.lastName = invoice_data['customer_data'][0]['last_name']
                customerAddress.company = invoice_data['customer_data'][0]['invoice_name']
                customerAddress.address = invoice_data['customer_data'][0]['line1']
                customerAddress.city = invoice_data['customer_data'][0]['city']
                customerAddress.state = invoice_data['customer_data'][0]['state_short']
                customerAddress.zip = invoice_data['customer_data'][0]['postal_code']
                customerAddress.country = "USA"

                customerData = apicontractsv1.customerDataType()
                customerData.type = 'individual'
                customerData.id = str(invoice_data['CustomerID'])
                customerData.email = 'example@example.com'

                duplicateWindowSetting = apicontractsv1.settingType()
                duplicateWindowSetting.settingName = "duplicateWindow"
                duplicateWindowSetting.settingValue = "600"
                settings_array = apicontractsv1.ArrayOfSetting()
                settings_array.setting.append(duplicateWindowSetting)

                line_items = apicontractsv1.ArrayOfLineItem()
                for line in invoice_data['lines']:
                    authorize_item = apicontractsv1.lineItemType()
                    authorize_item.itemId = str(line['UniqueID'])
                    authorize_item.name = str(line['PartNumber'])
                    authorize_item.description = line['Description']
                    authorize_item.quantity = str(line['QtyOrdered'])
                    authorize_item.unitPrice = str(line['UnitCost'])

                transactionrequest = apicontractsv1.transactionRequestType()
                transactionrequest.transactionType = "authCaptureTransaction"
                if form.cleaned_data['payment_type'] == 'full':
                    amount = context['limits']['max']
                else:
                    amount = form.cleaned_data['partial_value']
                transactionrequest.amount = str(amount)
                transactionrequest.payment = payment
                transactionrequest.order = order
                transactionrequest.billTo = customerAddress
                transactionrequest.customer = customerData
                transactionrequest.transactionSettings = settings_array
                transactionrequest.lineItems = line_items

                createtransactionrequest = apicontractsv1.createTransactionRequest()
                createtransactionrequest.merchantAuthentication = merchantAuth
                createtransactionrequest.refId = "TrailersPlus"
                createtransactionrequest.transactionRequest = transactionrequest

                createtransactioncontroller = createTransactionController(createtransactionrequest)
                createtransactioncontroller.setenvironment(constants.PRODUCTION)
                createtransactioncontroller.execute()

                response = createtransactioncontroller.getresponse()
                if response:
                    if hasattr(response, 'transactionResponse'):
                        response_code = response.transactionResponse.responseCode
                        auth_code = response.transactionResponse.authCode
                        trans_id = response.transactionResponse.transId
                        client_type = response.transactionResponse.accountType
                        if hasattr(response.transactionResponse, 'messages'):
                            message = response.transactionResponse.messages.message[0].description
                            context.update(
                                {"additional": {"success": True, "invalid_form": False}}
                            )
                        else:
                            message = response.transactionResponse.errors.error[0].errorText
                            context.update(
                                {"additional": {"success": False, "error": message, "invalid_form": False}}
                            )
                        client.add_payment_to_invoice(str(invoice_data['StoreID']),
                                                      int(invoice_data['InvoiceNumber']),
                                                      float(amount),
                                                      str(client_type),
                                                      str(response_code),
                                                      str(auth_code),
                                                      str(trans_id),
                                                      str(message))
                        return self.render_to_response(context)
                    else:
                        response_code = response.messages.message[0]['code'].text
                        message = response.messages.message[0]['text'].text
                        auth_code = None
                        trans_id = None
                        client.add_payment_to_invoice(str(invoice_data['StoreID']),
                                                      int(invoice_data['InvoiceNumber']),
                                                      float(amount),
                                                      None,
                                                      str(response_code),
                                                      auth_code,
                                                      trans_id,
                                                      str(message))
                        context.update(
                            {"additional": {"success": False, "error": message,"invalid_form": False}}
                        )
                        return self.render_to_response(context)
            except:
                context.update(
                    {"additional": {"success": False, "error": "Something goes wrong. Please try again later", "invalid_form": False}}
                )
                import traceback
                traceback.print_exc()
            return self.render_to_response(context)
        else:
            print('Invalid form')
            context.update({
                'additional': {
                    'success': False,
                    'invalid_form': True,
                }
            })
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(InvoiceView, self).get_context_data(**kwargs)
        client = WebsiteApiClient()
        invoice_from_link = client.invoice_from_link(kwargs.get('invoice_id'))
        try:
            error = invoice_from_link['error']
        except KeyError:
            pass
        else:
            if error:
                raise Http404
        invoice = client.invoice_data(invoice_from_link['StoreID'], invoice_from_link['InvoiceNumber'])
        limits = client.invoice_payment_limits(invoice_from_link['StoreID'], invoice_from_link['InvoiceNumber'])
        context.update(
            {
                "invoice": invoice,
                "limits": limits
            }
        )
        context.update({
            "subTotal": sum(line['ExtendedCost'] for line in invoice['lines'] if line['PartNumber'] != 'SALESTAX'),
            "balance": float(invoice['InvoiceValue']) - float(invoice['Collected'])
        })
        context.update({
            "additional": {"success": None, "invalid_form": None}
        })
        return context
