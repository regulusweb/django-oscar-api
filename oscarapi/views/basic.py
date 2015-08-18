import functools
import itertools

from django.contrib import auth
from oscar.core.loading import get_model, get_class
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixin import PutIsPatchMixin
from oscarapi import permissions
from oscarapi.basket.operations import assign_basket_strategy
from oscarapi.loading import get_api_class, get_api_classes


Selector = get_class('partner.strategy', 'Selector')

__all__ = (
    'BasketList', 'BasketDetail',
    'LineAttributeList', 'LineAttributeDetail',
    'ProductList', 'ProductDetail',
    'ProductPrice', 'ProductAvailability',
    'StockRecordList', 'StockRecordDetail',
    'UserList', 'UserDetail',
    'OptionList', 'OptionDetail',
    'CountryList', 'CountryDetail',
    'PartnerList', 'PartnerDetail',
)

Basket = get_model('basket', 'Basket')
LineAttribute = get_model('basket', 'LineAttribute')
Product = get_model('catalogue', 'Product')
StockRecord = get_model('partner', 'StockRecord')
Option = get_model('catalogue', 'Option')
User = auth.get_user_model()
Country = get_model('address', 'Country')
Partner = get_model('partner', 'Partner')

# checkout serializers
(CountrySerializer,
 PriceSerializer
 ) \
    = get_api_classes('oscarapi.serializers.checkout',
                      (
                          'CountrySerializer',
                          'PriceSerializer'
                      ))

# basket serializers
(BasketSerializer,
 LineAttributeSerializer,
 StockRecordSerializer
 ) \
    = get_api_classes('oscarapi.serializers.basket',
                      (
                          'BasketSerializer',
                          'LineAttributeSerializer',
                          'StockRecordSerializer'
                      ))

# product serializers
(ProductLinkSerializer,
 ProductSerializer,
 ProductAvailabilitySerializer,
 OptionSerializer,
 PartnerSerializer
 ) \
    = get_api_classes('oscarapi.serializers.product',
                      (
                          'ProductLinkSerializer',
                          'ProductSerializer',
                          'ProductAvailabilitySerializer',
                          'OptionSerializer',
                          'PartnerSerializer'
                      ))

UserSerializer = get_api_class('oscarapi.serializers.login', 'UserSerializer')


# TODO: For all API's in this file, the permissions should be checked if they
# are sensible.
class CountryList(generics.ListAPIView):
    serializer_class = CountrySerializer
    model = Country


class CountryDetail(generics.RetrieveAPIView):
    serializer_class = CountrySerializer
    model = Country


class BasketList(generics.ListCreateAPIView):
    model = Basket
    serializer_class = BasketSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        qs = super(BasketList, self).get_queryset()
        return itertools.imap(
            functools.partial(assign_basket_strategy, request=self.request), 
            qs)

class BasketDetail(PutIsPatchMixin, generics.RetrieveUpdateDestroyAPIView):
    model = Basket
    serializer_class = BasketSerializer
    permission_classes = (permissions.IsAdminUserOrRequestContainsBasket,)
    
    def get_object(self, queryset=None):
        basket = super(BasketDetail, self).get_object(queryset)
        return assign_basket_strategy(basket, self.request)

class LineAttributeList(generics.ListCreateAPIView):
    model = LineAttribute
    serializer_class = LineAttributeSerializer


class LineAttributeDetail(PutIsPatchMixin, generics.RetrieveAPIView):
    model = LineAttribute
    serializer_class = LineAttributeSerializer


class ProductList(generics.ListAPIView):
    model = Product
    serializer_class = ProductLinkSerializer


class ProductDetail(generics.RetrieveAPIView):
    model = Product
    serializer_class = ProductSerializer


class ProductPrice(APIView):

    def get(self, request, pk=None, format=None):
        product = Product.objects.get(id=pk)
        strategy = Selector().strategy(request=request, user=request.user)
        price = strategy.fetch_for_product(product).price
        ser = PriceSerializer(price,
                                          context={'request': request})
        return Response(ser.data)


class ProductAvailability(generics.RetrieveAPIView):
    model = Product
    serializer_class = ProductAvailabilitySerializer


class StockRecordList(generics.ListAPIView):
    model = StockRecord
    serializer_class = StockRecordSerializer

    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            self.queryset = self.get_queryset().filter(product__id=pk)

        return super(StockRecordList, self).get(request, *args, **kwargs)


class StockRecordDetail(generics.RetrieveAPIView):
    model = StockRecord
    serializer_class = StockRecordSerializer


class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class OptionList(generics.ListAPIView):
    model = Option
    serializer_class = OptionSerializer


class OptionDetail(generics.RetrieveAPIView):
    model = Option
    serializer_class = OptionSerializer


class PartnerList(generics.ListAPIView):
    model = Partner
    serializer_class = PartnerSerializer


class PartnerDetail(generics.RetrieveAPIView):
    model = Partner
    serializer_class = PartnerSerializer
