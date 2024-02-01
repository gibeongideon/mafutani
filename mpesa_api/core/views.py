from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from mpesa_api.core.tasks import (
    process_b2c_result_response_task,
    process_c2b_confirmation_task,
    process_c2b_validation_task,
    handle_online_checkout_callback_task,
)


class B2cTimeOut(APIView):
    """
    Handle b2c time out
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        return Response(dict(value="ok", key="status", detail="success"))


class B2cResult(APIView):
    """
    Handle b2c result
    
{
    "Result": {
        "ResultType": 0,
        "ResultCode": 0,
        "ResultDesc": "The service request has been accepted successfully.",
        "OriginatorConversationID": "19455-424535-1",
        "ConversationID": "AG_20170717_00006be9c8b5cc46abb6",
        "TransactionID": "LGH3197RIB",
        "ResultParameters": {
            "ResultParameter": [
                {"Key": "TransactionReceipt", "Value": "LGH3197RIB"},
                {"Key": "TransactionAmount", "Value": 8000},
                {"Key": "B2CWorkingAccountAvailableFunds", "Value": 150000},
                {"Key": "B2CUtilityAccountAvailableFunds", "Value": 133568},
                {"Key": "TransactionCompletedDateTime", "Value": "17.07.2017 10:54:57"},
                {"Key": "ReceiverPartyPublicName", "Value": "254708374149 - John Doe"},
                {"Key": "B2CChargesPaidAccountAvailableFunds", "Value": 0},
                {"Key": "B2CRecipientIsRegisteredCustomer", "Value": "Y"}
            ]
        },
        "ReferenceData": {
            "ReferenceItem": {
                "Key": "QueueTimeoutURL",
                "Value": "https://internalsandbox.safaricom.co.ke/mpesa/b2cresults/v1/submit"
            }
        }
    }
}
    
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the timeout
        :param request:
        :param format:
        :return:
        """
        data = request.data
        print(data)
        process_b2c_result_response_task(data)#TODO
        return Response(dict(value="ok", key="status", detail="success"))


class C2bValidation(APIView):
    """
    Handle c2b Validation
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the c2b Validation
        :param request:
        :param format:
        :return:
        """
        data = request.data
        process_c2b_validation_task(data)#TODO
        return Response(dict(value="ok", key="status", detail="success"))


class C2bConfirmation(APIView):
    """
    Handle c2b Confirmation
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the confirmation
        :param request:
        :param format:
        :return:
        """
        data = request.data
        process_c2b_confirmation_task(data)#TODO
        return Response(dict(value="ok", key="status", detail="success"))


class OnlineCheckoutCallback(APIView):
    """
    Handle online checkout callback
    """

    @csrf_exempt
    def post(self, request, format=None):
        """
        process the confirmation
        :param request:
        :param format:
        :return:
        
{
    "Result": {
        "ResultType": 0,
        "ResultCode": 0,
        "ResultDesc": "The service request has been accepted successfully.",
        "OriginatorConversationID": "19455-424535-1",
        "ConversationID": "AG_20170717_00006be9c8b5cc46abb6",
        "TransactionID": "LGH3197RIB",
        "ResultParameters": {
            "ResultParameter": [
                {"Key": "TransactionReceipt", "Value": "LGH3197RIB"},
                {"Key": "TransactionAmount", "Value": 8000},
                {"Key": "B2CWorkingAccountAvailableFunds", "Value": 150000},
                {"Key": "B2CUtilityAccountAvailableFunds", "Value": 133568},
                {"Key": "TransactionCompletedDateTime", "Value": "17.07.2017 10:54:57"},
                {"Key": "ReceiverPartyPublicName", "Value": "254708374149 - John Doe"},
                {"Key": "B2CChargesPaidAccountAvailableFunds", "Value": 0},
                {"Key": "B2CRecipientIsRegisteredCustomer", "Value": "Y"}
            ]
        },
        "ReferenceData": {
            "ReferenceItem": {
                "Key": "QueueTimeoutURL",
                "Value": "https://internalsandbox.safaricom.co.ke/mpesa/b2cresults/v1/submit"
            }
        }
    }
}  
        
        
        """
        response = request.data
        print(response)
        handle_online_checkout_callback_task(response)
        
        return Response(dict(value="ok", key="status", detail="success"))
