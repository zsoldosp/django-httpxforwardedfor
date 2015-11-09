# -*- coding: utf-8 -*-
from IPy import IP, parseAddress

from django.conf import settings


def is_valid_ip(ip):
    try:
        parseAddress(ip)
        return True
    except ValueError:
        return False


class XForwardedMiddleware(object):

    def __init__(self):
        self.trusted_ip_ranges = map(IP, settings.TRUSTED_PROXY_IPS)

    def process_request(self, request):
        if "HTTP_X_FORWARDED_FOR" in request.META:
            self._process_x_forwarded_for(request)

    def _process_x_forwarded_for(self, request):
        client_ips = request.META['HTTP_X_FORWARDED_FOR']
        proxy_ip = IP(request.META["REMOTE_ADDR"])

        if any(proxy_ip in trusted_ip_range for trusted_ip_range in self.trusted_ip_ranges):
            # client's IP will be the first valid one.
            client_ips = map(lambda i: i.strip(), client_ips.split(","))
            request.META['REMOTE_ADDR'] = filter(is_valid_ip, client_ips)[0]
        return
