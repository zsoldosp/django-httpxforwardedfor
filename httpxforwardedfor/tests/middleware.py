# -*- coding: utf-8 -*-
from hamcrest import assert_that, is_in

from django.conf import settings
from django.http import HttpRequest
from django.test.utils import override_settings
from django.utils import unittest

from paessler.httpxforwardedfor.middleware import HttpXForwardedForMiddleware


class HttpXForwardedForMiddlewareTestCase(unittest.TestCase):

    @override_settings(TRUSTED_PROXY_IPS=["1.1.1.1"])
    def test_x_forwarded_for_header_overrides_remote_addr(self):
        request = self.create_request(REMOTE_ADDR="1.1.1.1",
                                      HTTP_X_FORWARDED_FOR="1.2.3.4")
        self.assert_remote_addr_is("1.2.3.4", request)

    @override_settings(TRUSTED_PROXY_IPS=["1.1.1.1"])
    def test_x_forwarded_for_header_overrides_remote_addr__multiple_ips_in_header(self):
        request = self.create_request(REMOTE_ADDR="1.1.1.1",
                                      HTTP_X_FORWARDED_FOR="2.2.2.2, 3.3.3.3")
        self.assert_remote_addr_is("2.2.2.2", request)

    @override_settings(TRUSTED_PROXY_IPS=["2.2.2.2"])
    def test_x_forwarded_for_header_does_not_override_remote_addr_when_not_among_trusted_proxy_ips(self):
        request = self.create_request(REMOTE_ADDR="1.1.1.1",
                                      HTTP_X_FORWARDED_FOR="4.4.4.4")
        self.assert_remote_addr_is("1.1.1.1", request)

    @override_settings(TRUSTED_PROXY_IPS=["1.0/16"])
    def test_x_forwarded_for_header_overrides_remote_addr__iprange(self):
        request = self.create_request(REMOTE_ADDR="1.0.1.1",
                                      HTTP_X_FORWARDED_FOR="2.2.2.2")
        self.assert_remote_addr_is("2.2.2.2", request)

    @override_settings(TRUSTED_PROXY_IPS=["1.0/16"])
    def test_x_forwarded_for_header_overrides_remote_addr__multiple_ips_in_header__iprange(self):
        request = self.create_request(REMOTE_ADDR="1.0.1.1",
                                      HTTP_X_FORWARDED_FOR="2.2.2.2, 3.3.3.3")
        self.assert_remote_addr_is("2.2.2.2", request)

    @override_settings(TRUSTED_PROXY_IPS=["2.0/16"])
    def test_x_forwarded_for_header_does_not_override_remote_addr_when_not_among_trusted_proxy_ips__iprange(self):
        request = self.create_request(REMOTE_ADDR="1.1.1.1",
                                      HTTP_X_FORWARDED_FOR="4.4.4.4",)
        self.assert_remote_addr_is("1.1.1.1", request)

    @override_settings(TRUSTED_PROXY_IPS=["2.0/16", "1.0/16"])
    def test_x_forwarded_for_header_override_remote_addr__multiple_ips_in_header__multiple_trusted_ipranges(self):
        request = self.create_request(REMOTE_ADDR="1.0.1.1",
                                      HTTP_X_FORWARDED_FOR="2.2.2.2")
        self.assert_remote_addr_is("2.2.2.2", request)

    @override_settings(TRUSTED_PROXY_IPS=["2.0/16", "1.0/16"])
    def test_x_forwarded_for_header_not_present_does_not_change_remote_addr(self):
        request = self.create_request(REMOTE_ADDR="1.0.1.1")
        self.assert_remote_addr_is("1.0.1.1", request)

    @override_settings(TRUSTED_PROXY_IPS=["1.0.1.1"])
    def test_x_forwarded_for_header_no_valid_ip__multiple(self):
        request = self.create_request(REMOTE_ADDR="1.0.1.1",
                                      HTTP_X_FORWARDED_FOR="unknown, 2.2.2.2")
        self.assert_remote_addr_is("2.2.2.2", request)

    def test_x_forwarded_proto_is_recongnized_as_secure(self):
        request = self.create_request(HTTP_X_FORWARDED_PROTO="https")
        self.assertTrue(request.is_secure())

    def test_x_forwarded_proto_does_nothing_if_not_provided(self):
        request = self.create_request()
        self.assertFalse(request.is_secure())

    #####

    def assert_remote_addr_is(self, expected, request):
        self.assertEquals(expected, request.META["REMOTE_ADDR"])

    def create_request(self, path=None, **meta):
        path = path or "/"
        request = HttpRequest()
        request.META = {
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
        }
        request.META.update(**meta)
        request.path = request.path_info = path
        HttpXForwardedForMiddleware().process_request(request)
        return request


class HttpXForwardedForMiddlewareIntegrationTestCase(unittest.TestCase):
    MIDDLEWARE_NAME = "paessler.httpxforwardedfor.middleware.HttpXForwardedForMiddleware"

    def test__middleware_is_installed(self):
        assert_that(self.MIDDLEWARE_NAME, is_in(settings.MIDDLEWARE_CLASSES))

    def test__middleware_is_installed_before_all_other_middlewares_that_use_remote_addr(self):
        self.assertEquals(1, settings.MIDDLEWARE_CLASSES.index(self.MIDDLEWARE_NAME))
