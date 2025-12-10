from .base_provider import BaseLeadProvider
from faker import Faker
import random

class MockLeadProvider(BaseLeadProvider):
    """
    Generates realistic fake data for testing and demos.
    """
    def __init__(self):
        self.fake = Faker()

    def fetch_leads(self, industry: str, location: str, count: int = 5):
        leads = []
        for _ in range(count):
            leads.append({
                'company_name': f"{self.fake.company()} {industry}",
                'contact_name': self.fake.name(),
                'email': self.fake.company_email(),
                'phone': self.fake.phone_number(),
                'score': random.randint(50, 99) # Simulated AI Scoring
            })
        return leads
