from faker import Faker
import random
from models import db, Lead, LeadSearch

fake = Faker()

class LeadService:
    @staticmethod
    def generate_leads(user_id, industry, location, count=5):
        # Create Search Record
        search = LeadSearch(user_id=user_id, industry=industry, location=location)
        db.session.add(search)
        db.session.commit()

        leads = []
        for _ in range(count):
            lead = Lead(
                search_id=search.id,
                company_name=f"{fake.company()} {industry}",
                contact_name=fake.name(),
                email=fake.company_email(),
                phone=fake.phone_number(),
                score=random.randint(50, 99)
            )
            db.session.add(lead)
            leads.append(lead)

        db.session.commit()
        return search.id, leads

    @staticmethod
    def get_leads_by_search(search_id):
        return Lead.query.filter_by(search_id=search_id).all()
