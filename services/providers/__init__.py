from .mock_provider import MockLeadProvider
from .external_provider import ExternalAPILeadProvider
import os

def get_lead_provider():
    """
    Factory function to return the configured provider.
    """
    provider_type = os.environ.get('LEAD_PROVIDER', 'MOCK').upper()

    if provider_type == 'EXTERNAL':
        api_key = os.environ.get('LEAD_API_KEY', '')
        return ExternalAPILeadProvider(api_key=api_key)
    else:
        return MockLeadProvider()
