from os import path
from uuid import uuid4

import ujson as json  #use this library from pip - it will take care of the datetime serialization and everything
from redis import StrictRedis

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
from django.conf import settings


REDIS_CONN_STRING = settings.REDIS_MESSAGE
COMMAND_QUEUE = 'WEBSITE_API_CLIENT'
RESPONSE_TIMEOUT = 30 #30 seconds
REDIS_CA_CERT = settings.ROOT('trailersplus', 'certs', 'redis', 'aiven_ca.pem', required=True)


class WebsiteApiClient(object):

    def __init__(self):
        self.redis = StrictRedis.from_url(REDIS_CONN_STRING, ssl_ca_certs=REDIS_CA_CERT)

    def _make_call(self, function, args):
        import pprint
        print("Strarting redis call")
        print("Generating key")
        key = str(uuid4())
        print(f"{key=}")
        print(f"Pushing {function=} with next args")
        pprint.pprint(args)
        self.redis.rpush(COMMAND_QUEUE, json.dumps({'function': function, 'args': args, 'key': key}))
        print("W8ting for response")
        data = self.redis.blpop(key, RESPONSE_TIMEOUT)
        if not data:
            raise RuntimeError('Timeout - No response from redis api')
        data = json.loads(data[1])
        return data

    def trailer_status(self, VIN):
        """ example return data
        {u'status': 150, u'status_verbose': u'Sold'}
        """
        return self._make_call('trailer_status', [VIN])

    def get_or_create_customer(self, invoice_name, first_name, last_name, title, email_address, phone_number,
                               address_1, address_2, city, state_short, postal_code, country, language='English'):
        """ language is 'English' or 'Spanish'
        invoice_name is either company name or customer full name
        example return data
        {'customer_id': cust_id}
        """
        return self._make_call(
            'get_or_create_customer',
            [invoice_name, first_name, last_name, title, email_address, phone_number,
             address_1, address_2, city, state_short, postal_code, country, language]
        )

    def customer_active_reserves(self, customer_id):
        """ this function is to check if a customer has an active reserve already
        (we only allow one at a time)
        example return data
        {'active_reserves': 0}
        if its more than 0 don't allow customer to reserve another trailer
        """
        return self._make_call('customer_active_reserves', [customer_id])

    def create_invoice(self, customer_id, store_id, VIN):
        """ example return data
        {'error': True, 'message': 'Error - trailer not available', 'store_id': None, 'invoice_number': None}
        {'error': False, 'message': 'Success', 'store_id': store_id, 'invoice_number': inv_no}
        """
        return self._make_call('create_invoice', [customer_id, store_id, VIN])

    def invoice_data(self, store_id, invoice_number):
        """example return data
        ***PLEASE DO NOT DISPLAY THE NOTE FIELDS TO THE CUSTOMER***

        {
            'CashPriceInvoice': 0,
            'Collected': Decimal('0.00'),
            'CompleteDate': None,
            'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
            'CustomerID': 1697723L,
            'CustomerName': u'JOHN WATSON',
            'CustomerPicture': None,
            'DiscountedTrailer': Decimal('7249.00'),
            'Due': Decimal('7249.00'),
            'EditDate': datetime.datetime(2020, 11, 10, 12, 51, 56),
            'InvoiceNumber': 32047L,
            'InvoiceValue': Decimal('7249.00'),
            'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
            'SalesPerson2Active': None,
            'SalesPerson2Email': None,
            'SalesPerson2LoginID': None,
            'SalesPerson2Name': None,
            'SalesPerson2Number': None,
            'SalesPerson2UserID': None,
            'SalesPersonActive': 0,
            'SalesPersonEmail': None,
            'SalesPersonLoginID': u'TRAILERSPLUS\\weblead',
            'SalesPersonName': u'Web Lead',
            'SalesPersonNumber': u'0',
            'SalesPersonUserID': u'weblead',
            'Status': 1,
            'StatusDescription': u'Quote',
            'StoreID': u'TRPL35',
            'VIN': None,
            'lines': [{'CompleteDate': None,
              'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'Description': u'7 x 16 Loadrunner 7K',
              'EditDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'ExtendedCost': Decimal('10509.00'),
              'InvoiceDate': None,
              'InvoiceNumber': 32047L,
              'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'PartNumber': u'ILRD716TA2',
              'QtyDelivered': Decimal('1.00'),
              'QtyOrdered': Decimal('1.00'),
              'SerialNumber': u'4RALS1623MK075899',
              'StoreID': u'TRPL35',
              'Taxable': 0,
              'UniqueID': 25301348L,
              'UnitCost': Decimal('10509.00'),
              'Units': u'EACH'},
             {'CompleteDate': None,
              'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'Description': u'Dealer Discount Pre-approved',
              'EditDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'ExtendedCost': Decimal('-3260.00'),
              'InvoiceDate': None,
              'InvoiceNumber': 32047L,
              'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'PartNumber': u'DISCOUNT',
              'QtyDelivered': Decimal('1.00'),
              'QtyOrdered': Decimal('1.00'),
              'SerialNumber': None,
              'StoreID': u'TRPL35',
              'Taxable': 0,
              'UniqueID': 25301349L,
              'UnitCost': Decimal('-3260.00'),
              'Units': u'EACH'},
             {'CompleteDate': None,
              'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'Description': u'Sale price Approved By luteyns Approved Sale Price HD Coupler Lock Required On The Lot',
              'EditDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'ExtendedCost': Decimal('0.00'),
              'InvoiceDate': None,
              'InvoiceNumber': 32047L,
              'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'PartNumber': u'NOTE',
              'QtyDelivered': Decimal('1.00'),
              'QtyOrdered': Decimal('1.00'),
              'SerialNumber': None,
              'StoreID': u'TRPL35',
              'Taxable': 0,
              'UniqueID': 25301350L,
              'UnitCost': Decimal('0.00'),
              'Units': u'EACH'}]
        }
        """
        return self._make_call('invoice_data', [store_id, invoice_number])

    def invoice_from_link(self, link_id):
        """link_id will come from the URL we email to the customer
        (example: https://www.trailersplus.com/invoice/1c31469f20d541d4a7847e95bcf999a6
            link_id would be 1c31469f20d541d4a7847e95bcf999a6 )
        return data will be the same as invoice_data function
            or if no invoice is found it will return
        {'error': True, 'message': "Couldn't find invoice"}
        """
        return self._make_call('invoice_from_link', [link_id])

    def add_reserve_to_invoice(self, store_id, invoice_number, response_code, auth_code, trans_id, messages):
        """please submit these wether they were successful or not
            i will add the messages as a note on unsuccessful ones for our salespeople to see
        NOTE: This is the "authorize only" transaction, do not capture it.
        example return data
        {'error': False, 'message': 'Success.'}
        """
        return self._make_call('add_reserve_to_invoice',
                               [store_id, invoice_number, response_code, auth_code, trans_id, messages])

    def invoice_payment_limits(self, store_id, invoice_number):
        """Use this to limit the max/minimum that an online payment can be for each invoice
        example return data:
        {'max': 0, 'min': 0}
        {'max': 1000, 'min': 250}
        """
        return self._make_call('invoice_payment_limits', [store_id, invoice_number])

    def add_payment_to_invoice(self, store_id, invoice_number, payment_amount, card_type, response_code,
                               auth_code, trans_id, messages):
        """Use this function to add auth & capture payments to the invoice
        example return data:
        True
        """
        return self._make_call('add_payment_to_invoice', [store_id, invoice_number, payment_amount, card_type,
                                                          response_code, auth_code, trans_id, messages])



"""
Flow for trailer reserve:
1) get_or_create_customer & store the returned customer_id
2) trailer_status - to make sure trailer is still available
3) customer_active_reserves - to make sure customer doesn't already have another trailer reserved
4) create_invoice  - save store_id and invoice_number
5) do the transaction with authorize.net (authorize only transaction)
6) add_reserve_to_invoice - this will add the reserve in our system and update the status of the trailer in our system


Flow for invoice payment:
1) our agents email special links to our customers like https://www.trailersplus.com/invoice/1c31469f20d541d4a7847e95bcf999a6
2) invoice_from_link - get store_id and invoice_number
3) invoice_data - pull to display to customer
4) invoice_payment_limits - to get min/max the customer can pay (can be 0 for invoices that have already had a payment applied)
5) do the transaction with authorize.net (auth & capture type transaction)
6) add_payment_to_invoice - submit result from #5
"""
