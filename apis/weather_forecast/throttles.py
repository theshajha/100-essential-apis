from rest_framework.throttling import ScopedRateThrottle


class CustomScopedRateThrottle(ScopedRateThrottle):
    THROTTLE_RATES = {
        'daily': '100/day',
        'hourly': '30/hour',
        'minute': '10/minute'
    }

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
