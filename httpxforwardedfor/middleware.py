# -*- coding: utf-8 -*-
from IPy import IP, parseAddress

from django.conf import settings


class HttpXForwardedForMiddleware(object):

    def __init__(self):
        self.TRUSTED_PROXY_IP_RANGES = map(IP, settings.TRUSTED_PROXY_IPS)

    def process_request(self, request):
        if "HTTP_X_FORWARDED_FOR" not in request.META:
            return  # No HTTP_X_FORWARDED_FOR header, nothimng to do
        if not self._request_via_trusted_proxy(request):
            return  # We don't accept HTTP_X_FORWARDED_FOR from other proxies
        client_ips = self._get_valid_client_ip_addresses(request)
        if not client_ips:
            return  # No valid IP left
        request.META['REMOTE_ADDR'] = client_ips[0]

    def _request_via_trusted_proxy(self, request):
        """Check, if the IP in REMPTE_ADDR belongs to a trusted proxy"""
        remote_addr = IP(request.META["REMOTE_ADDR"])
        return any(remote_addr in trusted_ip_range
                   for trusted_ip_range in self.TRUSTED_PROXY_IP_RANGES)

    def _get_valid_client_ip_addresses(self, request):
        """Get all valid IP addresses from the HTTP_X_FORWARDED_FOR header"""

        def _is_valid_ip(ip):
            """Check for valid IP address"""
            try:
                parseAddress(ip)
                return True
            except ValueError:
                return False

        client_ips = request.META['HTTP_X_FORWARDED_FOR'].split(",")
        return [s.strip() for s in client_ips if _is_valid_ip(s.strip())]
