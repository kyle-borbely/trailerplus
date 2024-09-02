import datetime as dt

from authorizenet import apicontractsv1
from authorizenet.constants import constants
from authorizenet.apicontrollers import createTransactionController
from django.conf import settings
from rest_framework import viewsets
from django.db import transaction

from checkout.models import TestInvoice
from .serializers import LocationSerializer
from product.models import Location, Trailer
from django.utils.translation import get_language
from .permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, CSRFCheck
from rest_framework.pagination import PageNumberPagination, replace_query_param
from rest_framework.views import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from .models import ProductReviews
from math import ceil
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.backends.db import SessionStore
from checkout.services import WebsiteApiClient

from .models import LowerPrice, Appointment, Custom, Fleet

from .serializers import (
    LowerPriceSerializer,
    AppointmentSerializer,
    CustomSerializer,
    FleetSerializer,
    ProductReviewsSerializer
)

import json
from .tasks import save_review
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import HttpResponse
from my_store.models import get_store_trailers


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(active=True)
    serializer_class = LocationSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, *args, **kwargs):
        if get_language() == 'es':
            titles = {
                "get_direction_title": "Obtener las Direcciones",
                "view_store_invent_title": "Ver Inventario de la Tienda",
                "set_store_title": "Establecer Como mi Tienda",
                "more_information_title": "Más información",
                "store_hours_title": "Horarios",
            }
        else:
            titles = {
                "get_direction_title": "Get Directions",
                "view_store_invent_title": "View Store Inventory",
                "set_store_title": "Set Store as Default",
                "more_information_title": "More Information",
                "store_hours_title": "Store Hours",
            }
        response = {
            "locations": sorted(self.serializer_class(
                self.get_queryset(), many=True, context=self.get_serializer_context()
            ).data, key=lambda x: x['store_city']),
            "titles": titles,
        }
        return Response(response)

    def get_serializer_context(self):
        locale = get_language()
        context = super(LocationViewSet, self).get_serializer_context()
        context.update({"locale": locale, "request": self.request})
        return context


class ProductReviewsPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 6

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        page_number = ceil(self.page.paginator.count / self.page_size)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        page_number = 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'first': self.get_first_link(),
                'last': self.get_last_link(),
            },
            'count': self.page.paginator.count,
            'last_page_number': ceil(self.page.paginator.count / self.page_size),
            'results': data
        })


class ProductReviewsList(ListAPIView):
    serializer_class = ProductReviewsSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductReviewsPagination

    # def list(self, request, trailer_vin, *args, **kwargs):
    #     queryset = Trailer.objects.prefetch_related('reviews').get(vin=trailer_vin).reviews.all()
    #     result_page = self.pagination_class.paginate_queryset(queryset, request)
    #     serializer = ProductReviewsSerializer(result_page, many=True)
    #     return self.pagination_class.get_paginated_response(serializer.data)

    def get_queryset(self):
        trailers = Trailer.objects.get(vin=self.request.query_params['vin'])
        reviews = ProductReviews.objects.filter(products=trailers)[6:]
        return reviews


class LowerPriceCreate(CreateAPIView):
    queryset = LowerPrice.objects.all()
    serializer_class = LowerPriceSerializer
    permission_classes = [AllowAny]


class AppointmentCreate(CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]


class CustomCreate(CreateAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerializer
    permission_classes = [AllowAny]


class FleetCreate(CreateAPIView):
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    permission_classes = [AllowAny]


class TrailersCount(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        store_city = request.query_params.get('trailer-store', None)
        try:
            location = Location.objects.prefetch_related('trailer_set').get(store_city=store_city)
        except ObjectDoesNotExist:
            if store_city is not None:
                return Response({'trailer-store': f'Store "{store_city}" Does Not Exist'})
            else:
                return Response({'trailer-store': 'Required'})
        trailer_type = request.query_params.get('trailer-type', 'all')
        if trailer_type != 'all':
            trailers = get_store_trailers(location).filter(category__category_map__slug=trailer_type).count()
        else:
            trailers = get_store_trailers(location).trailer_set.count()
        return Response({'location': store_city, 'type': trailer_type, 'count': trailers})


class CartSession(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        session_id = request.POST.get('sessionid')
        # cart_item = request.POST.get('cart_item')
        cart_item = request.data['cart_item']
        request.session['cart_item'] = cart_item
        request.session.modified = True
        # session = SessionStore(session_key=session_id)
        # if session.pop('cart_item', False):
        #     status_code = 204
        # else:
        #     status_code = 201
        # session['cart_item'] = cart_item
        # session.save()
        return Response({session_id: {"cart_item": cart_item}}, status=201)

    def delete(self, request):
        session_id = request.POST.get('sessionid')
        del request.session['cart_item']
        request.session.modified = True
        # session = SessionStore(session_key=session_id)
        # session.pop('cart_item')
        # session.save()
        return Response({"Deleted successfully": 204}, status=204)


class UserLocation(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        session_id = request.POST.get('sessionid')
        # location_id = request.POST.get('location_id')
        location_id = request.data['location_id']
        request.session['user_location'] = location_id
        request.session.modified = True
        # session = SessionStore(session_key=session_id)
        # session.pop('user_location', None)
        # session['user_location'] = location_id
        # session.save()
        return Response({session_id: {"location_id": location_id}})


@csrf_exempt
@require_POST
def review_create(request):
    json_data = request.body
    data = json.loads(json_data)
    for event in data["events"]:
        save_review.delay(event["eventName"], event['eventData'])
    return HttpResponse(status=201)


class CheckoutView(CreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        try:
            redis_conn = WebsiteApiClient()
            data = request.data
            print(f"{data=}")
            redis_language = 'Spanish' if get_language() == 'es' else 'English'
            print(f"{redis_language=}")
            trailer = Trailer.objects.select_related('store').prefetch_related('trailertranslation_set').get(
                vin=data['trailer_id'])
            print(f"{trailer=}")
            trailer_verbose = trailer.trailertranslation_set.get(language=get_language().upper()).short_description
            print(f"{trailer_verbose=}")
            customer_id = redis_conn.get_or_create_customer(
                invoice_name=data['company'] or ' '.join((data['firstname'], data['lastname'])),
                first_name=data['firstname'],
                last_name=data['lastname'],
                title=trailer_verbose,
                email_address=data['email'],
                phone_number=data['phone'],
                address_1=data['address'],
                address_2=None,
                city=request.data['city'],
                state_short=request.data['state'],
                postal_code=request.data['zip'],
                country='USA',
                language=redis_language
            )['customer_id']
            print(f"{customer_id=}")
            trailer_status = redis_conn.trailer_status(data['trailer_id'])
            print(trailer_status)
            if int(trailer_status['status']) != 100:
                return Response(
                    {"error": f"Sorry this trailer is already {trailer_status['status_verbose'].lower()}"},
                    status=400)
            customer_active_reserves = redis_conn.customer_active_reserves(customer_id)['active_reserves']
            if int(customer_active_reserves) > 0:
                return Response(
                    {"error": "You already have reserved trailer"},
                    status=400
                )
            created_invoice = redis_conn.create_invoice(
                customer_id=customer_id,
                store_id=trailer.store.store_id,
                VIN=data['trailer_id']
            )
            print(f"{created_invoice=}")
            invoice_creation_error = bool(created_invoice.get('error', False))
            if invoice_creation_error:
                return Response(
                    {"error": created_invoice['message']},
                    status=400
                )
            invoice_number = created_invoice['invoice_number']

            # AUTHORIZE TRANSACTION
            merchantAuth = apicontractsv1.merchantAuthenticationType()
            merchantAuth.name = settings.AUTHORIZE_LOGIN_ID
            merchantAuth.transactionKey = settings.AUTHORIZE_TRANSACTION_KEY

            creditCard = apicontractsv1.creditCardType()
            creditCard.cardNumber = request.data['cardnumber'].replace('-', '')
            expirity = request.data['expirity'].split('/')
            creditCard.expirationDate = f"20{expirity[1]}-{expirity[0]}"
            creditCard.cardCode = request.data['ccv']

            payment = apicontractsv1.paymentType()
            payment.creditCard = creditCard

            order = apicontractsv1.orderType()
            order.invoiceNumber = f"{trailer.store.store_id}-{invoice_number}"
            order.description = trailer_verbose

            customerAddress = apicontractsv1.customerAddressType()
            customerAddress.firstName = request.data['firstname']
            customerAddress.lastName = request.data['lastname']
            customerAddress.company = data['company'] or ' '.join((data['firstname'], data['lastname']))
            customerAddress.address = request.data['address']
            customerAddress.city = request.data['city']
            customerAddress.state = request.data['state']
            customerAddress.zip = request.data['zip']
            customerAddress.country = "USA"

            customerData = apicontractsv1.customerDataType()
            customerData.type = "business" if request.POST['company'] else "individual"
            customerData.id = str(customer_id)
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
            createtransactioncontroller.setenvironment(constants.PRODUCTION)
            createtransactioncontroller.execute()

            response = createtransactioncontroller.getresponse()
            if response:
                if hasattr(response, 'transactionResponse'):
                    response_code = response.transactionResponse.responseCode
                    auth_code = response.transactionResponse.authCode
                    trans_id = response.transactionResponse.transId
                    if hasattr(response.transactionResponse, 'messages'):
                        message = response.transactionResponse.messages.message[0].description
                        status_code = 200
                        TestInvoice.objects.create(
                            invoice_id=invoice_number,
                            trailer=trailer,
                            customer_email=data['email'],
                            date=dt.datetime.now()
                        )
                        request.session['last_invoice'] = invoice_number
                        del request.session['cart_item']
                        request.session.modified = True
                    else:
                        message = response.transactionResponse.errors.error[0].errorText
                        status_code = 400
                    redis_conn.add_reserve_to_invoice(trailer.store.store_id, invoice_number, str(response_code), str(auth_code),
                                                      str(trans_id), str(message))
                    response_message = {"message": str(message)} if status_code == 200 else {"error": str(message)}
                    return Response(
                        response_message,
                        status=status_code
                    )
                else:
                    response_code = response.messages.message[0]['code'].text
                    message = response.messages.message[0]['text'].text
                    auth_code = None
                    trans_id = None
                    redis_conn.add_reserve_to_invoice(trailer.store_id, invoice_number, str(response_code), auth_code,
                                                      trans_id, str(message))
                    return Response(
                        {"error": str(message)},
                        status=400
                    )

        except RuntimeError:
            return Response(
                {"error": "Ooops! Something went wrong"},
                status=409
            )
