from .base_provider import BaseLeadProvider
import requests
import json

class PDLLeadProvider(BaseLeadProvider):
    """
    Integration with People Data Labs (PDL) Person Search API.
    Requires PDL_API_KEY environment variable.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.peopledatalabs.com/v5/person/search"

    def fetch_leads(self, industry: str, location: str, count: int = 5):
        """
        Searches for people using PDL SQL query.
        """
        if not self.api_key:
            print("Error: PDL_API_KEY is missing.")
            return []

        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }

        # Construct SQL Query
        # We use flexible LIKE matching for industry and location to increase hit rate
        sql_query = f"""
            SELECT * FROM person
            WHERE job_company_industry LIKE '%{industry}%'
            AND location_name LIKE '%{location}%'
            AND emails IS NOT NULL
        """

        payload = {
            "sql": sql_query,
            "size": count,
            "pretty": True
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=payload)
            response.raise_for_status()
            data = response.json()
            return self._parse_response(data)
        except requests.exceptions.RequestException as e:
            print(f"PDL API Request Failed: {e}")
            return []

    def _parse_response(self, data):
        results = []
        # PDL returns a 'data' array of profiles
        profiles = data.get('data', [])

        for person in profiles:
            # PDL returns 'emails' as a list of objects with 'address'
            emails = person.get('emails', [])
            email = emails[0].get('address') if emails else "N/A"

            # PDL returns 'phone_numbers' as a list of strings (sometimes) or objects
            # Checking documentation: it's often a list of strings in simplified response,
            # but let's handle the list safely.
            phones = person.get('phone_numbers', [])
            phone = phones[0] if phones else "N/A"

            lead = {
                'company_name': person.get('job_company_name', 'Unknown Company'),
                'contact_name': person.get('full_name', 'Unknown Contact'),
                'email': email,
                'phone': phone,
                'score': self._calculate_score(person)
            }
            results.append(lead)

        return results

    def _calculate_score(self, person):
        # Calculate quality score based on data richness
        score = 60
        if person.get('work_email'): score += 15
        if person.get('mobile_phone'): score += 15
        if person.get('linkedin_url'): score += 10
        return min(score, 100)
