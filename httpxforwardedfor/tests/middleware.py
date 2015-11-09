# -*- coding: utf-8 -*-
from django.utils import unittest

from django.conf import settings
from django.http import HttpRequest
from django.test.client import Client

from paessler.httpxforwardedfor.middleware import XForwardedMiddleware


class MiddlewareTestCase(object):

    def setUp(self):
        super(MiddlewareTestCase, self).setUp()
        self.client = Client()

    def _create_request(self, path):
        request = HttpRequest()
        request.META = {
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
        }
        request.path = request.path_info = path
        return request

    def get_middleware_from_decorated_view(self, decorated_view):
        return decorated_view.func_closure[0].cell_contents.__class__

    @staticmethod
    def assert_contains(haystack, needle):
        assert needle in haystack, "Could not find '%s' in '%s'" % (needle, haystack)


class XForwardedMiddlewareTestCase(MiddlewareTestCase, unittest.TestCase):

    def setUp(self):
        super(XForwardedMiddlewareTestCase, self).setUp()
        self.retained_trusted_proxies = settings.TRUSTED_PROXY_IPS

    def tearDown(self):
        super(XForwardedMiddlewareTestCase, self).tearDown()
        settings.TRUSTED_PROXY_IPS = self.retained_trusted_proxies

    def test_x_forwarded_for_header_overrides_remote_addr(self):
        settings.TRUSTED_PROXY_IPS = ["1.1.1.1"]
        self.assertEquals("1.2.3.4", self.process_request_and_get_resulting_remote_addr(
            REMOTE_ADDR="1.1.1.1",
            HTTP_X_FORWARDED_FOR="1.2.3.4",
        ))

    def test_x_forwarded_for_header_overrides_remote_addr__multiple_ips_in_header(self):
        settings.TRUSTED_PROXY_IPS = ["1.1.1.1"]
        self.assertEquals("2.2.2.2", self.process_request_and_get_resulting_remote_addr(
            REMOTE_ADDR="1.1.1.1",
            HTTP_X_FORWARDED_FOR="2.2.2.2, 3.3.3.3"
        ))

    def test_x_forwarded_for_header_does_not_override_remote_addr_when_not_among_trusted_proxy_ips(self):
        settings.TRUSTED_PROXY_IPS = ["2.2.2.2"]
        self.assertEquals("1.1.1.1", self.process_request_and_get_resulting_remote_addr(
            REMOTE_ADDR="1.1.1.1",
            HTTP_X_FORWARDED_FOR="4.4.4.4"
        ))

    def test_x_forwarded_for_header_overrides_remote_addr__iprange(self):
        settings.TRUSTED_PROXY_IPS = ["1.0/16"]
        self.assertEquals("2.2.2.2", self.process_request_and_get_resulting_remote_addr(
            REMOTE_ADDR="1.0.1.1",
            HTTP_X_FORWARDED_FOR="2.2.2.2"
        ))

    def test_x_forwarded_for_header_overrides_remote_addr__multiple_ips_in_header__iprange(self):
        settings.TRUSTED_PROXY_IPS = ["1.0/16"]
        self.assertEquals("2.2.2.2", self.process_request_and_get_resulting_remote_addr(
            REMOTE_ADDR="1.0.1.1",
            HTTP_X_FORWARDED_FOR="2.2.2.2, 3.3.3.3"
        ))

    def test_x_forwarded_for_header_does_not_override_remote_addr_when_not_among_trusted_proxy_ips__iprange(self):
        settings.TRUSTED_PROXY_IPS = ["2.0/16"]
        self.assertEquals("1.1.1.1", self.process_request_and_get_resulting_remote_addr(
            REMOTE_ADDR="1.1.1.1",
            HTTP_X_FORWARDED_FOR="4.4.4.4",
        ))

    def test_x_forwarded_for_header_override_remote_addr__multiple_ips_in_header__multiple_trusted_ipranges(self):
        settings.TRUSTED_PROXY_IPS = ["2.0/16", "1.0/16"]
        self.assertEquals("2.2.2.2", self.process_request_and_get_resulting_remote_addr(
            REMOTE_ADDR="1.0.1.1",
            HTTP_X_FORWARDED_FOR="2.2.2.2",
        ))

    def test_x_forwarded_for_header_not_present_does_not_change_remote_addr(self):
        settings.TRUSTED_PROXY_IPS = ["2.0/16", "1.0/16"]
        self.assertEquals("1.0.1.1", self.process_request_and_get_resulting_remote_addr(
            REMOTE_ADDR="1.0.1.1",
        ))

    def test_x_forwarded_for_header_no_valid_ip__multiple(self):
        settings.TRUSTED_PROXY_IPS = ["1.0.1.1"]
        self.assertEquals("2.2.2.2", self.process_request_and_get_resulting_remote_addr(
            REMOTE_ADDR="1.0.1.1",
            HTTP_X_FORWARDED_FOR="unknown, 2.2.2.2",
        ))

    def test_x_forwarded_proto_is_recongnized_as_secure(self):
        request, response = self.create_request_and_response()
        request.META.update(dict(HTTP_X_FORWARDED_PROTO="https"))

        self.assertTrue(request.is_secure())

    def test_x_forwarded_proto_does_nothing_if_not_provided(self):
        request, response = self.create_request_and_response()
        self.assertFalse(request.is_secure())

    def process_request_and_get_resulting_remote_addr(self, **meta):
        request, response = self.create_request_and_response()

        request.META.update(meta)
        XForwardedMiddleware().process_request(request)
        return request.META["REMOTE_ADDR"]

    def create_request_and_response(self, data=None, path=None):
        path = path or "/"
        data = data or dict()
        request = self._create_request(path)
        response = self.client.get(path, data=data)
        return request, response


class XForwardedForMiddlewareIntegrationTestCase(MiddlewareTestCase, unittest.TestCase):

    def test__middleware_is_installed(self):
        middleware_name = "paessler.httpxforwardedfor.middleware.XForwardedMiddleware"
        self.assert_contains(settings.MIDDLEWARE_CLASSES, middleware_name)

    def test__middleware_is_installed_before_all_other_middlewares_that_use_remote_addr(self):
        middleware_name = "paessler.httpxforwardedfor.middleware.XForwardedMiddleware"
        self.assertEquals(1, settings.MIDDLEWARE_CLASSES.index(middleware_name))
