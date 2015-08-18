from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from oscarapi.loading import get_api_classes, get_api_class


LoginView = get_api_class('oscarapi.views.login', 'LoginView')

# basket views
(BasketView,
 AddProductView,
 add_voucher,
 shipping_methods,
 LineList,
 LineDetail
 ) \
    = get_api_classes('oscarapi.views.basket',
                      (
                          'BasketView',
                          'AddProductView',
                          'add_voucher',
                          'shipping_methods',
                          'LineList',
                          'LineDetail'
                      ))
# basic views
(LineAttributeList,
 LineAttributeDetail,
 ProductList,
 ProductDetail,
 ProductPrice,
 ProductAvailability,
 StockRecordList,
 StockRecordDetail,
 OptionList,
 OptionDetail,
 UserList,
 UserDetail,
 CountryList,
 CountryDetail,
 PartnerList,
 PartnerDetail,
 BasketList,
 BasketDetail
 ) \
    = get_api_classes('oscarapi.views.basic',
                    (
                        'LineAttributeList',
                        'LineAttributeDetail',
                        'ProductList',
                        'ProductDetail',
                        'ProductPrice',
                        'ProductAvailability',
                        'StockRecordList',
                        'StockRecordDetail',
                        'OptionList',
                        'OptionDetail',
                        'UserList',
                        'UserDetail',
                        'CountryList',
                        'CountryDetail',
                        'PartnerList',
                        'PartnerDetail',
                        'BasketList',
                        'BasketDetail'
                    ))

# checkout views
(CheckoutView,
 OrderList,
 OrderDetail,
 OrderLineList,
 OrderLineDetail,
 OrderLineAttributeDetail
 ) \
    = get_api_classes('oscarapi.views.checkout',
                     (
                         'CheckoutView',
                         'OrderList',
                         'OrderDetail',
                         'OrderLineList',
                         'OrderLineDetail',
                         'OrderLineAttributeDetail'
                     ))

urlpatterns = patterns('',
    url(r'^$', 'oscarapi.views.api_root', name='api-root'),
    url(r'^login/$', LoginView.as_view(), name='api-login'),
    url(r'^basket/$', BasketView.as_view(), name='api-basket'),
    url(r'^basket/add-product/$', AddProductView.as_view(), name='api-basket-add-product'),
    url(r'^basket/add-voucher/$', add_voucher, name='api-basket-add-voucher'),
    url(r'^basket/shipping-methods/$', shipping_methods, name='api-basket-shipping-methods'),
    url(r'^baskets/(?P<pk>[0-9]+)/lines/$', LineList.as_view(), name='basket-lines-list'),
    url(r'^baskets/$', BasketList.as_view(), name='basket-list'),
    url(r'^baskets/(?P<pk>[0-9]+)/$', BasketDetail.as_view(), name='basket-detail'),
    url(r'^lines/$', LineList.as_view(), name='line-list'),
    url(r'^lines/(?P<pk>[0-9]+)/$', LineDetail.as_view(), name='line-detail'),
    url(r'^lineattributes/$', LineAttributeList.as_view(), name='lineattribute-list'),
    url(r'^lineattributes/(?P<pk>[0-9]+)/$', LineAttributeDetail.as_view(), name='lineattribute-detail'),
    url(r'^products/$', ProductList.as_view(), name='product-list'),
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetail.as_view(), name='product-detail'),
    url(r'^products/(?P<pk>[0-9]+)/price/$', ProductPrice.as_view(), name='product-price'),
    url(r'^products/(?P<pk>[0-9]+)/availability/$', ProductAvailability.as_view(), name='product-availability'),
    url(r'^products/(?P<pk>[0-9]+)/stockrecords/$', StockRecordList.as_view(), name='product-stockrecord-list'),
    url(r'^stockrecords/$', StockRecordList.as_view(), name='stockrecord-list'),
    url(r'^stockrecords/(?P<pk>[0-9]+)/$', StockRecordDetail.as_view(), name='stockrecord-detail'),
    url(r'^options/$', OptionList.as_view(), name='option-list'),
    url(r'^options/(?P<pk>[0-9]+)/$', OptionDetail.as_view(), name='option-detail'),
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'^checkout/$', CheckoutView.as_view(), name='api-checkout'),
    url(r'^orders/$', OrderList.as_view(), name='order-list'),
    url(r'^orders/(?P<pk>[0-9]+)/$', OrderDetail.as_view(), name='order-detail'),
    url(r'^orders/(?P<pk>[0-9]+)/lines/$', OrderLineList.as_view(), name='order-lines-list'),
    url(r'^orderlines/(?P<pk>[0-9]+)/$', OrderLineDetail.as_view(), name='order-lines-detail'),
    url(r'^orderlineattributes/(?P<pk>[0-9]+)/$', OrderLineAttributeDetail.as_view(), name='order-lineattributes-detail'),
    url(r'^countries/$', CountryList.as_view(), name='country-list'),
    url(r'^countries/(?P<pk>[A-z]+)/$', CountryDetail.as_view(), name='country-detail'),
    url(r'^partners/$', PartnerList.as_view(), name='partner-list'),
    url(r'^partners/(?P<pk>[0-9]+)/$', PartnerDetail.as_view(), name='partner-detail')
)

urlpatterns = format_suffix_patterns(urlpatterns)
