from .base_provider import BaseLeadProvider
import requests
import os

class ApolloLeadProvider(BaseLeadProvider):
    """
    Integration with Apollo.io API for real B2B contact data.
    Requires APOLLO_API_KEY environment variable.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.apollo.io/v1/mixed_people/search"

    def fetch_leads(self, industry: str, location: str, count: int = 5):
        """
        Searches for people based on Industry (Keywords) and Location.
        """
        if not self.api_key:
            print("Error: APOLLO_API_KEY is missing.")
            return []

        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": self.api_key
        }

        # Apollo API Payload Construction
        # Note: 'industry' in Apollo is often a specific ID, but we can search by "q_organization_keyword_tags"
        # or "person_titles" or generic keywords.
        # For this MVP, we map 'industry' to a keyword search.

        payload = {
            "q_organization_keyword_tags": [industry],
            "person_locations": [location],
            "page": 1,
            "per_page": count,
            "person_titles": ["CEO", "Founder", "Owner", "Manager"] # Default to decision makers
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_response(data)
        except requests.exceptions.RequestException as e:
            print(f"Apollo API Request Failed: {e}")
            return []

    def _parse_response(self, data):
        results = []
        people = data.get('people', [])

        for person in people:
            # Safely extract nested fields
            org = person.get('organization') or {}

            # Construct formatted lead
            lead = {
                'company_name': org.get('name', 'Unknown Company'),
                'contact_name': f"{person.get('first_name', '')} {person.get('last_name', '')}".strip(),
                'email': person.get('email') or "N/A",
                'phone': person.get('phone_numbers', [None])[0] or "N/A", # Grab first phone if available
                # Calculate a mock score based on data completeness
                'score': self._calculate_score(person)
            }
            results.append(lead)

        return results

    def _calculate_score(self, person):
        score = 50
        if person.get('email'): score += 20
        if person.get('phone_numbers'): score += 20
        if person.get('linkedin_url'): score += 10
        return min(score, 100)
