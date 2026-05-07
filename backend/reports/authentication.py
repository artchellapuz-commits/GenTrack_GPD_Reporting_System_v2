"""Custom authentication classes"""
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Session authentication without CSRF enforcement.
    Use this for development or when CSRF is handled elsewhere.
    """
    def enforce_csrf(self, request):
        """
        Override to skip CSRF check
        """
        return  # Do nothing, skip CSRF check
