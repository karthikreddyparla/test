from models import db, Lead, LeadSearch
from services.providers import get_lead_provider

class LeadService:
    @staticmethod
    def generate_leads(user_id, industry, location, count=5):
        # 1. Create Search Record (Audit Log)
        search = LeadSearch(user_id=user_id, industry=industry, location=location)
        db.session.add(search)
        db.session.commit()

        # 2. Get Data from the configured Provider
        provider = get_lead_provider()
        raw_leads = provider.fetch_leads(industry, location, count)

        # 3. Persist and Normalize Data
        leads = []
        for item in raw_leads:
            lead = Lead(
                search_id=search.id,
                company_name=item.get('company_name'),
                contact_name=item.get('contact_name'),
                email=item.get('email'),
                phone=item.get('phone'),
                score=item.get('score', 0)
            )
            db.session.add(lead)
            leads.append(lead)

        db.session.commit()
        return search.id, leads

    @staticmethod
    def get_leads_by_search(search_id):
        return Lead.query.filter_by(search_id=search_id).all()
