from .base_provider import BaseLeadProvider
import requests
import random

class ExternalAPILeadProvider(BaseLeadProvider):
    """
    Skeleton for a real data provider (e.g., Apollo.io, Clearbit).
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Example API Endpoint
        self.base_url = "https://api.example-data-provider.com/v1/search"

    def fetch_leads(self, industry: str, location: str, count: int = 5):
        """
        In a real scenario, this would make an HTTP Request.
        """
        # Example Payload
        payload = {
            'api_key': self.api_key,
            'industry': industry,
            'location': location,
            'limit': count
        }

        # response = requests.post(self.base_url, json=payload)
        # if response.status_code == 200:
        #     return self._parse_response(response.json())

        # Fallback for now since we don't have a real key
        print(f"Warning: External API called without valid key. Returning empty list.")
        return []

    def _parse_response(self, data):
        # Map external API fields to our internal format
        results = []
        for item in data.get('matches', []):
            results.append({
                'company_name': item.get('org_name'),
                'contact_name': item.get('full_name'),
                'email': item.get('email'),
                'phone': item.get('phone'),
                'score': random.randint(60, 90) # Or calculate based on data completeness
            })
        return results
