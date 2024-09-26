
from django.urls import path,include
from .views import PaymentMethodView

urlpatterns = [
    path('payment-method/', PaymentMethodView.as_view())
    

]
