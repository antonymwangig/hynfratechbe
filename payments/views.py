from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Payment
from .utils import mask_card_number
# Create your views here.

class PaymentMethodView(APIView):
    def get(self, request):
        user = request.user
        payment = Payment.objects.all().order_by("-payment_date").first()
        
        return Response({
            "id":payment.id,
            "card_number":mask_card_number(payment.card_number),
            "card_type":payment.card_type
        })