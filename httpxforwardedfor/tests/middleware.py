# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.test.utils import override_settings

from httpxforwardedfor.middleware import HttpXForwardedForMiddleware


class HttpXForwardedForMiddlewareTestScenarios(object):
    MIDDLEWARE_NAME = "httpxforwardedfor.middleware.HttpXForwardedForMiddleware"

    def setUp(self):
        super(HttpXForwardedForMiddlewareTestScenarios, self).setUpClass()
        self.assertIn(self.MIDDLEWARE_NAME, settings.MIDDLEWARE_CLASSES)

    def test_header_overrides_remote_addr_for_trusted_proxy_ip__single_ip_in_header(self):
        request = self.create_request(REMOTE_ADDR="1.1.1.1",
                                      HTTP_X_FORWARDED_FOR="1.2.3.4")
        self.assert_remote_addr_is("1.2.3.4", request)

    def test_header_overrides_remote_addr_for_trusted_proxy_ip__multiple_ips_in_header(self):
        request = self.create_request(REMOTE_ADDR="1.1.1.1",
                                      HTTP_X_FORWARDED_FOR="2.2.2.2, 12.12.12.12, 3.3.3.3")
        self.assert_remote_addr_is("3.3.3.3", request)

    def test_header_overrides_remote_addr_for_trusted_proxy_ip__multiple_ips_with_invalid_string_in_header(self):
        request = self.create_request(REMOTE_ADDR="1.1.1.1",
                                      HTTP_X_FORWARDED_FOR="unknown, 12.12.12.12, 2.2.2.2")
        self.assert_remote_addr_is("2.2.2.2", request)

    def test_header_does_not_override_remote_addr_for_untrusted_proxy_ip(self):
        request = self.create_request(REMOTE_ADDR="9.9.9.9",
                                      HTTP_X_FORWARDED_FOR="4.4.4.4")
        self.assert_remote_addr_is("9.9.9.9", request)

    def test_header_not_present_does_not_change_remote_addr(self):
        request = self.create_request(REMOTE_ADDR="1.0.1.1")
        self.assert_remote_addr_is("1.0.1.1", request)

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
            "SERVER_NAME": "testserver",
            "SERVER_PORT": 80,
        }
        request.META.update(**meta)
        request.path = request.path_info = path
        HttpXForwardedForMiddleware().process_request(request)
        return request


@override_settings(TRUSTED_PROXY_IPS=["1.1.1.1"])
class SingleTrustedProxyIpTestCase(HttpXForwardedForMiddlewareTestScenarios,
                                   SimpleTestCase):
    pass


@override_settings(TRUSTED_PROXY_IPS=["1.1.1.1", "1.2.3.4"])
class MultipleTrustedProxyIpTestCase(HttpXForwardedForMiddlewareTestScenarios,
                                     SimpleTestCase):
    pass


@override_settings(TRUSTED_PROXY_IPS=["1.1/16"])
class SingleTrustedProxyIpRangeTestCase(HttpXForwardedForMiddlewareTestScenarios,
                                        SimpleTestCase):
    pass


@override_settings(TRUSTED_PROXY_IPS=["1.1/16", "1.2/16"])
class MultipleTrustedProxyIpRangeTestCase(HttpXForwardedForMiddlewareTestScenarios,
                                          SimpleTestCase):
    pass
