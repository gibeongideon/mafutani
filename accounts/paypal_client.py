# import os
import sys
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment,LiveEnvironment
from django.conf import settings


import os

# import json
import random
import string
from paypalpayoutssdk.payouts import PayoutsPostRequest


# Creating an environment
client_id = settings.PAYPAL_CLIENT_ID
if settings.DEBUG:
    environment = SandboxEnvironment(client_id=client_id, client_secret=settings.PAYPAL_CLIENT_SECRET)
else:
    environment = LiveEnvironment(client_id=client_id, client_secret=settings.PAYPAL_CLIENT_SECRET)

client = PayPalHttpClient(environment)



class PayPalClient:
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        
        """Setting up and Returns PayPal SDK environment with PayPal Access credentials.
           For demo purpose, we are using SandboxEnvironment. In production this will be
           LiveEnvironment."""
        if settings.DEBUG:
            self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        else:
            self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        
        """ Returns PayPal HTTP client instance with environment which has access
            credentials context. This can be used invoke PayPal API's provided the
            credentials have the access to do so. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key,value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result
    
    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, bytes) or isinstance(data, int)








class CreatePayouts(PayPalClient):

    """ Creates a payout batch with 5 payout items
    Calls the create batch api (POST - /v1/payments/payouts)
    A maximum of 15000 payout items are supported in a single batch request"""

    def __init__(self, amount, receiver):
        self.amount = amount
        self.receiver = receiver
        PayPalClient.__init__(self)

    # @staticmethod
    def build_request_body(self, include_validation_failure = False):
        senderBatchId = str(''.join(random.sample(
            string.ascii_uppercase + string.digits, k=7)))
        amount = self.amount # if include_validation_failure else "1.00"
        return \
            {
                "sender_batch_header": {
                    "recipient_type": "EMAIL",
                    "email_message": "Darius Option Win Payout",
                    "note": "Enjoy your Payout!!",
                    "sender_batch_id": senderBatchId,
                    "email_subject": "Darius Spin Wins Payout.Enjoy!"
                },
                "items": [{
                    "note": "Thanks for playing Darius Wheel.Refer more for more payout!",
                    "amount": {
                        "currency": "USD",
                        "value": amount
                    },
                    "receiver": self.receiver,
                    "sender_item_id": "PayoutD"
                }]
            }

    def create_payouts(self, debug=False):
        request = PayoutsPostRequest()
        request.request_body(self.build_request_body(False))
        response = self.client.execute(request)

        if debug:
            print("Status Code: ", response.status_code)
            print("Payout Batch ID: " +
                  response.result.batch_header.payout_batch_id)
            print("Payout Batch Status: " +
                  response.result.batch_header.batch_status)
            print("Links: ")
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(
                    link.rel, link.href, link.method))

            # To toggle print the whole body comment/uncomment the below line
            #json_data = self.object_to_json(response.result)
            #print "json_data: ", json.dumps(json_data, indent=4)

        return response
