from .mock_provider import MockLeadProvider
from .external_provider import ExternalAPILeadProvider
from .apollo_provider import ApolloLeadProvider
from .pdl_provider import PDLLeadProvider
import os

def get_lead_provider():
    """
    Factory function to return the configured provider.
    """
    provider_type = os.environ.get('LEAD_PROVIDER', 'MOCK').upper()

    # Check for specific keys first, or generic one
    api_key = os.environ.get('LEAD_API_KEY', '')
    pdl_key = os.environ.get('PDL_API_KEY', api_key)
    apollo_key = os.environ.get('APOLLO_API_KEY', api_key)

    if provider_type == 'APOLLO':
        return ApolloLeadProvider(api_key=apollo_key)
    elif provider_type == 'PDL':
        return PDLLeadProvider(api_key=pdl_key)
    elif provider_type == 'EXTERNAL':
        return ExternalAPILeadProvider(api_key=api_key)
    else:
        return MockLeadProvider()
