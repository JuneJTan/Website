from ipaddress import ip_address, ip_network

from django.conf import settings
from django.http import HttpResponseForbidden


class AdminIPAllowlistMiddleware:
    """Restrict Django admin access to configured IP ranges."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_networks = [
            ip_network(cidr) for cidr in getattr(settings, "ADMIN_ALLOWED_IP_RANGES", [])
        ]

    def __call__(self, request):
        if request.path.startswith("/admin/") and not self._is_allowed(request):
            return HttpResponseForbidden("Forbidden: admin access is restricted.")
        return self.get_response(request)

    def _is_allowed(self, request):
        if not self.allowed_networks:
            return True

        client_ip = self._client_ip(request)
        if not client_ip:
            return False

        try:
            parsed_ip = ip_address(client_ip)
        except ValueError:
            return False

        return any(parsed_ip in network for network in self.allowed_networks)

    def _client_ip(self, request):
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")
