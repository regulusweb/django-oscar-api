import sys
import os

from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings

from oscar.core.loading import (
    AppNotFoundError, ClassNotFoundError)

from oscarapi.loading import get_api_class, get_api_classes

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class LoadingTestCase(TestCase):

    def setUp(self):
        # add the tests directory (which contains the test apps) to the path
        sys.path.append(TEST_DIR)

    def tearDown(self):
        sys.path.remove(TEST_DIR)


class TestClassLoading(LoadingTestCase):
    """
    Oscar's class loading utilities
    """

    def test_load_oscar_classes_correctly(self):
        HeaderSessionMiddleware, ApiGatewayMiddleWare = get_api_classes('oscarapi.middleware',
                                                                        ('HeaderSessionMiddleware',
                                                                         'ApiGatewayMiddleWare'))
        self.assertEqual('oscarapi.middleware', HeaderSessionMiddleware.__module__)
        self.assertEqual('oscarapi.middleware', ApiGatewayMiddleWare.__module__)

    def test_load_oscar_class_correctly(self):
        HeaderSessionMiddleware = get_api_class('oscarapi.middleware', 'HeaderSessionMiddleware')
        self.assertEqual('oscarapi.middleware', HeaderSessionMiddleware.__module__)

    def test_raise_exception_when_bad_appname_used(self):
        with self.assertRaises(AppNotFoundError):
            get_api_classes('fridge.models', ('ApiKey', 'ApiKey2'))

    def test_raise_exception_when_bad_classname_used(self):
        with self.assertRaises(ClassNotFoundError):
            get_api_class('oscarapi.models', 'Monkey')

    def test_raise_importerror_if_app_raises_importerror(self):
        """
        This tests that Oscar doesn't fall back to using the Oscar catalogue
        app if the overriding app throws an ImportError.
        """
        apps = list(settings.INSTALLED_APPS)
        apps[apps.index('oscarapi')] = 'test_apps.oscarapi'
        with override_settings(INSTALLED_APPS=apps):
            with self.assertRaises(ImportError):
                get_api_class('oscarapi.middleware', 'HeaderSessionMiddleware')


class ClassLoadingWithLocalOverrideTests(LoadingTestCase):

    def setUp(self):
        super(ClassLoadingWithLocalOverrideTests, self).setUp()
        self.installed_apps = list(settings.INSTALLED_APPS)
        self.installed_apps[self.installed_apps.index('oscarapi')] = 'test_apps.oscarapi'

    def test_loading_class_defined_in_local_module(self):
        with override_settings(INSTALLED_APPS=self.installed_apps):
            (BasketLineSerializer,) = get_api_classes('oscarapi.serializers.basket', ('BasketLineSerializer',))
            self.assertEqual('test_apps.oscarapi.serializers.basket', BasketLineSerializer.__module__)

    def test_loading_class_which_is_not_defined_in_local_module(self):
        with override_settings(INSTALLED_APPS=self.installed_apps):
            (BasketSerializer,) = get_api_classes('oscarapi.serializers.basket', ('BasketSerializer',))
            self.assertEqual('oscarapi.serializers.basket', BasketSerializer.__module__)

    def test_loading_class_from_module_not_defined_in_local_app(self):
        with override_settings(INSTALLED_APPS=self.installed_apps):
            (PriceSerializer,) = get_api_classes('oscarapi.serializers.checkout', ('PriceSerializer',))
            self.assertEqual('oscarapi.serializers.checkout', PriceSerializer.__module__)

    def test_loading_classes_defined_in_both_local_and_oscar_modules(self):
        with override_settings(INSTALLED_APPS=self.installed_apps):
            (BasketLineSerializer, BasketSerializer) = get_api_classes('oscarapi.serializers.basket',
                                                                       ('BasketLineSerializer', 'BasketSerializer'))
            self.assertEqual('test_apps.oscarapi.serializers.basket', BasketLineSerializer.__module__)
            self.assertEqual('oscarapi.serializers.basket', BasketSerializer.__module__)


class ClassLoadingWithLocalOverrideWithMultipleSegmentsTests(LoadingTestCase):

    def setUp(self):
        super(ClassLoadingWithLocalOverrideWithMultipleSegmentsTests, self).setUp()
        self.installed_apps = list(settings.INSTALLED_APPS)
        self.installed_apps[self.installed_apps.index('oscarapi')] = 'test_apps.apps.oscarapi'

    def test_loading_class_defined_in_local_module(self):
        with override_settings(INSTALLED_APPS=self.installed_apps):
            (BasketLineSerializer,) = get_api_classes('oscarapi.serializers.basket', ('BasketLineSerializer',))
            self.assertEqual('test_apps.apps.oscarapi.serializers.basket', BasketLineSerializer.__module__)
